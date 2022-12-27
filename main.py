import os.path

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from backend.auth_utils import hash_password, verify_password, new_token, auth
from backend.database_utils import execute, drop_database, create_database
from backend.models import user, ws_stock, ws_position
from backend.models.ws_position import WSPosition
from backend.models.ws_stock import WSStock
from backend.models.user import User
from backend.payloads.login import Login
from backend.repository import Repository
from backend.wealthsimple_utils import WealthSimpleAPI

if not os.path.exists('frontend/dist'):
    os.mkdir('frontend/dist')

# Connecting WealthSimple
TOTP_SECRET = os.environ.get('TOTP_SECRET', 'blopblopblop')
WS_ACCOUNT = os.environ.get('WS_ACCOUNT', 'test@bob.com:mypassword')
WS_TFSA_ID = os.environ.get('WS_TFSA_ID', 'blopblop')

email, password = WS_ACCOUNT.split(':', 1)
ws = WealthSimpleAPI(email, password, TOTP_SECRET)
ws.set_account(WS_TFSA_ID)

# Init Database
DROP_DB = os.environ.get('DROP_DB', 'false') == 'true'
if DROP_DB:
    drop_database('trade_tracker')

try:
    create_database('trade_tracker')
except:
    pass

# Create Tables
execute(user.SQL_SCHEMA, fetch=False)
execute(ws_stock.SQL_SCHEMA, fetch=False)
execute(ws_position.SQL_SCHEMA, fetch=False)

# Repositories
users = Repository('user', User)
stocks = Repository('stock', WSStock)
positions = Repository('position', WSPosition)

# Create Super Admin
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'blopblopblop')
admin = next(users.find('username', 'admin'), None)
if admin is None:
    admin = User(1, 'admin', hash_password(ADMIN_PASSWORD), 'super_admin')
users.upsert(admin)

# Init Watchlist Stocks
watchlist_stocks = ws.watchlist()
stocks.truncate()
for w_stock in watchlist_stocks:
    stocks.upsert(w_stock)

# Init Positions
ws_positions = ws.positions()
positions.truncate()
for position in ws_positions:
    positions.upsert(position)

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


@fastapi.get('/api/v1/watchlist', dependencies=[auth('default')])
def watchlist_get():
    return stocks.list()


@fastapi.get('/api/v1/watchlist/update', dependencies=[auth('default')])
def watchlist_set():
    watchlist_stocks = ws.watchlist()
    stocks.truncate()
    for w_stock in watchlist_stocks:
        stocks.upsert(w_stock)

    return stocks.list()


@fastapi.get('/api/v1/positions', dependencies=[auth('default')])
def positions_get():
    return positions.list()


@fastapi.get('/api/v1/positions/update', dependencies=[auth('default')])
def positions_set():
    ws_positions = ws.positions()
    positions.truncate()
    for position in ws_positions:
        positions.upsert(position)

    return positions.list()


fastapi.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
