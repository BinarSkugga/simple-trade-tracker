import pytest

from database_utils import execute, drop_database, create_database
from models import user, ws_stock, ws_position
from repository import Repository
from tests.mocked_wealthsimple_api import MockedWealthSimpleAPI


@pytest.fixture(autouse=True)
def initialize_schema():
    drop_database('trade_tracker_test')
    create_database('trade_tracker_test')

    execute(user.SQL_SCHEMA, fetch=False)
    execute(ws_stock.SQL_SCHEMA, fetch=False)
    execute(ws_position.SQL_SCHEMA, fetch=False)


@pytest.fixture
def mocked_ws_api():
    return MockedWealthSimpleAPI()


@pytest.fixture
def user_repository():
    return Repository('user', user.User)


@pytest.fixture
def stock_repository():
    return Repository('stock', ws_stock.WSStock)


@pytest.fixture
def position_repository():
    return Repository('position', ws_position.WSPosition)
