import os.path

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from auth_utils import hash_password, verify_password, new_token, auth
from database_utils import execute, drop_database, create_database
from models import ws_stock, user
from models.ws_stock import WSStock
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

# Init Database
DROP_DB = os.environ.get('DROP_DB', 'false') == 'true'
if DROP_DB:
    drop_database('trade_tracker')
    create_database('trade_tracker')

# Create Tables
execute(user.SQL_SCHEMA, fetch=False)
execute(ws_stock.SQL_SCHEMA, fetch=False)

# Repositories
users = Repository('user', User)
stocks = Repository('stock', WSStock)

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
def watchlist():
    return stocks.list()


@fastapi.get('/api/v1/watchlist/update', dependencies=[auth('default')])
def watchlist_set():
    watchlist_stocks = ws.watchlist()
    stocks.truncate()
    for w_stock in watchlist_stocks:
        stocks.upsert(w_stock)


fastapi.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
