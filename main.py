import os.path

from fastapi import FastAPI
from psycopg import DatabaseError
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from backend.auth_utils import hash_password
from backend.database_utils import execute, drop_database, create_database
from backend.models import user, stock, ws_position
from backend.models.ws_position import WSPosition
from backend.models.stock import Stock
from backend.models.user import User
from backend.repository import Repository
from backend.wealthsimple_utils import WealthSimpleAPI
from config import WS_ACCOUNT, TOTP_SECRET, WS_TFSA_ID, DROP_DB
from routes import auth_routes, stock_routes, position_routes
from utils import create_dist_folder

email, password = WS_ACCOUNT.split(':', 1)
ws = WealthSimpleAPI(email, password, TOTP_SECRET)
ws.set_account(WS_TFSA_ID)

# Init Database
try:
    if DROP_DB:
        drop_database('trade_tracker')
    create_database('trade_tracker')
except DatabaseError as e:
    print(f'Couldn\'t create or drop database: {e}')

# Create Tables
execute(user.SQL_SCHEMA, fetch=False)
execute(stock.SQL_SCHEMA, fetch=False)
execute(ws_position.SQL_SCHEMA, fetch=False)

# Create Repositories
users = Repository('user', User)
stocks = Repository('stock', Stock)
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
    allow_headers=["*"]
)


auth_routes.load(fastapi)
stock_routes.load(fastapi, ws)
position_routes.load(fastapi, ws)

create_dist_folder('frontend/dist')
fastapi.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
