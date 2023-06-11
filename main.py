import os.path

from fastapi import FastAPI
from psycopg import DatabaseError
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from backend.auth_utils import hash_password
from backend.database_utils import execute, drop_database, create_database
from backend.models import user, stock, ws_position, activity
from backend.models.ws_position import WSPosition
from backend.models.stock import Stock
from backend.models.user import User
from backend.repository import Repository
from backend.models.activity import Activity
from backend.wealthsimple_utils import WealthSimpleAPI
from backend.config import WS_ACCOUNT, TOTP_SECRET, WS_TFSA_ID, DROP_DB
from backend.routes import auth_routes, stock_routes, position_routes, activity_routes
from backend.utils import create_dist_folder

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
execute(activity.SQL_SCHEMA, fetch=False)

# Create Repositories
users = Repository('user', User)
stocks = Repository('stock', Stock)
positions = Repository('position', WSPosition)
activities = Repository('activity', Activity)

# Create Super Admin
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'blopblopblop')
admin = next(users.find('username', 'admin'), None)
if admin is None:
    admin = User(1, 'admin', hash_password(ADMIN_PASSWORD), 'super_admin')
users.upsert(admin)

# Init Watchlist Stocks
current_stocks = list(stocks.list())

if len(current_stocks) == 0:
    watchlist_stocks = ws.watchlist()
    for w_stock in watchlist_stocks:
        stocks.upsert(w_stock)

# Init Positions
current_positions = list(positions.list())

if len(current_positions) == 0:
    ws_positions = ws.positions()
    for position in ws_positions:
        positions.upsert(position)

# Init Activities
current_activities = list(activities.list())

if len(current_activities) == 0:
    ws_activities = ws.activities()
    for activity in ws_activities:
        activities.upsert(activity)

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
activity_routes.load(fastapi, ws)

create_dist_folder('frontend/dist')
fastapi.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
