import os.path
import time

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from auth_utils import hash_password, verify_password, new_token, auth
from database_utils import execute
from models import stock, portfolio, portfolio_entry, user
from models.portfolio import Portfolio, portfolio_dumper
from models.portfolio_entry import PortfolioEntry
from models.stock import Stock
from models.user import User
from payloads.login import Login
from repository import Repository
from wealthsimple_utils import WealthSimpleAPI

if not os.path.exists('frontend/dist'):
    os.mkdir('frontend/dist')

# Connecting WealthSimple
TOTP_SECRET = os.environ.get('TOTP_SECRET', 'blopblopblop')
WS_ACCOUNT = os.environ.get('WS_ACCOUNT', 'test@bob.com:mypassword')
WS_TFSA_ID = os.environ.get('WS_TFSA_ID', 'blopblop')

email, password = WS_ACCOUNT.split(':', 1)
ws = WealthSimpleAPI(email, password, TOTP_SECRET)
ws.set_account(WS_TFSA_ID)


# Create Tables
execute(user.SQL_SCHEMA, False)
execute(stock.SQL_SCHEMA, False)
execute(portfolio.SQL_SCHEMA, False)
execute(portfolio_entry.SQL_SCHEMA, False)

# Repositories
users = Repository('user', User)
stocks = Repository('stock', Stock)
portfolios = Repository('portfolio', Portfolio, model_dumper=portfolio_dumper)
portfolio_entries = Repository('portfolio_entry', PortfolioEntry)

# Create Super Admin
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'blopblopblop')
admin = next(users.find('username', 'admin'), None)
if admin is None:
    admin = User(0, 'admin', hash_password(ADMIN_PASSWORD), 'super_admin')
users.upsert(admin)

# Fake Stocks
dfn = {"short_name": "DIVIDEND 15 SPLIT CORP", "long_name": "Dividend 15 Split Corp.", "symbol": "DFN.TO",
       "sector": "Financial Services", "exchange": "TOR", "timezone": "America/Toronto", "currency": "CAD",
       "price": 7.18, "beta": 1.591541, "dividend_yield": 0.1693, "ex_dividend_date": 1666915200,
       "payout_ratio": 1.0619, "debt_equity_ratio": 1.747, "monthly_return": 0.10129783333333332}
div = {"short_name": "DIVERSIFIED ROYALTY CORP", "long_name": "Diversified Royalty Corp.", "symbol": "DIV.TO",
       "sector": "Industrials", "exchange": "TOR", "timezone": "America/Toronto", "currency": "CAD", "price": 2.92,
       "beta": 1.595824, "dividend_yield": 0.081599995, "ex_dividend_date": 1665619200, "payout_ratio": 1.0356,
       "debt_equity_ratio": 1.692, "monthly_return": 0.019855998783333332}
stocks.upsert(Stock(id=1, **dfn))
stocks.upsert(Stock(id=2, **div))

# Fake Portfolios
port1 = {"name": 'Test Portfolio 1', "user_id": 0}
port2 = {"name": 'Test Portfolio 2', "user_id": 0}
# port3 = {"name": 'Test Portfolio 3', "user_id": 1}

portfolios.upsert(Portfolio(id=1, **port1))
portfolios.upsert(Portfolio(id=2, **port2))
# portfolios.upsert(Portfolio(id=3, **port3))

# Fake Entries
entry001 = {"portfolio_id": 1, "stock_id": 2, "count": 200, "strike": 2.18, "date": time.time() - 56}  # Bought 10 DIV in port1 at $2.18
entry002 = {"portfolio_id": 1, "stock_id": 1, "count": 29, "strike": 7.89, "date": time.time() - 45}  # Bought 5 DFN in port1 at $7.89
entry003 = {"portfolio_id": 1, "stock_id": 1, "count": -2, "strike": 7.56, "date": time.time() - 20}  # Sold 2 DFN in port1 for $7.56

portfolio_entries.upsert(PortfolioEntry(id=1, **entry001))
portfolio_entries.upsert(PortfolioEntry(id=2, **entry002))
portfolio_entries.upsert(PortfolioEntry(id=3, **entry003))

# Create FastAPI
fastapi = FastAPI()

fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@fastapi.post('/api/v1/login')
def login(payload: Login):
    user: User = next(users.find('username', payload.username), None)
    if user is None:
        raise HTTPException(401, 'bad login')
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, 'bad login')

    return {'access_token': new_token({'id': user.id}, 0)}


@fastapi.get('/api/v1/me', dependencies=[auth('default')])
def me(request: Request):
    return request.scope['user']


@fastapi.get('/api/v1/stocks', dependencies=[auth('default')])
def list_stocks():
    stocks_data = list(stocks.list())
    return stocks_data


@fastapi.get('/api/v1/portfolios', dependencies=[auth('default')])
def get_my_portfolios(request: Request):
    portfolios_data = list(portfolios.find('user_id', request.scope['user'].id))
    entries = list(portfolio_entries.find('portfolio_id', [port.id for port in portfolios_data]))
    for port in portfolios_data:
        port.entries = [e for e in entries if e.portfolio_id == port.id]

    return portfolios_data


fastapi.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
