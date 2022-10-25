import os.path

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from auth_utils import hash_password, verify_password, new_token, auth
from database_utils import execute
from models import stock, portfolio, portfolio_entry, user
from models.portfolio import Portfolio
from models.portfolio_entry import PortfolioEntry
from models.stock import Stock
from models.user import User
from payloads.login import Login
from repository import Repository

if not os.path.exists('frontend/dist'):
    os.mkdir('frontend/dist')

# Create Tables
execute(user.SQL_SCHEMA, False)
execute(stock.SQL_SCHEMA, False)
execute(portfolio.SQL_SCHEMA, False)
execute(portfolio_entry.SQL_SCHEMA, False)

# Repositories
users = Repository('user', User)
stocks = Repository('stock', Stock)
portfolios = Repository('portfolio', Portfolio)
portfolio_entries = Repository('portfolio_entry', PortfolioEntry)

# Create Super Admin
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'blopblopblop')
admin = next(users.find('username', 'admin'), None)
if admin is None:
    admin = User(0, 'admin', hash_password(ADMIN_PASSWORD), 'super_admin')
users.upsert(admin)

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
    return stocks.list()


@fastapi.get('/api/v1/portfolios', dependencies=[auth('default')])
def get_my_portfolios(request: Request):
    return portfolios.find('user_id', request.scope['user'].id)


fastapi.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
