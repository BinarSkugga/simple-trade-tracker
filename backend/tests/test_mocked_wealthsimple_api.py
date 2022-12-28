import time

import pytest

from backend.interface.wealthsimple_api_interface import FailedWSLogin
from backend.models.ws_position import WSPosition
from backend.models.stock import Stock
from backend.models.ws_token_set import WSTokenSet


def test_login_success(mocked_ws_api):
    token_set = mocked_ws_api.login('test01@gmail.com', 'blopblopblop', '789523')

    assert isinstance(token_set, WSTokenSet)
    assert token_set.access == 'master_access'
    assert token_set.refresh == 'master_refresh'
    assert token_set.expire == pytest.approx(time.time() + mocked_ws_api.expiry, 0.1)


def test_login_bad_password(mocked_ws_api):
    with pytest.raises(FailedWSLogin):
        mocked_ws_api.login('test01@gmail.com', 'blopblopblop1', '789523')


def test_login_bad_otp(mocked_ws_api):
    with pytest.raises(FailedWSLogin):
        mocked_ws_api.login('test02@gmail.com', 'blopblopblop', '789623')


def test_login_bad_user(mocked_ws_api):
    with pytest.raises(FailedWSLogin):
        mocked_ws_api.login('test06@gmail.com', 'blopblopblop', '789523')


def test_refresh_success(mocked_ws_api):
    mocked_ws_api.login('test01@gmail.com', 'blopblopblop', '789523')
    token_set = mocked_ws_api.refresh('master_refresh')

    assert isinstance(token_set, WSTokenSet)
    assert token_set.access == 'master_access'
    assert token_set.refresh == 'master_refresh'
    assert token_set.expire == pytest.approx(time.time() + mocked_ws_api.expiry, 0.1)


def test_refresh_not_logged(mocked_ws_api):
    with pytest.raises(FailedWSLogin):
        mocked_ws_api.refresh('master_refresh')


def test_refresh_bad_token(mocked_ws_api):
    with pytest.raises(FailedWSLogin):
        mocked_ws_api.refresh('naster_refresh')


def test_watchlist_success(mocked_ws_api):
    mocked_ws_api.login('test01@gmail.com', 'blopblopblop', '789523')
    stocks = mocked_ws_api.watchlist()

    assert isinstance(stocks, list)
    assert len(stocks) == 10
    assert all([isinstance(s, Stock) for s in stocks])


def test_watchlist_not_logged(mocked_ws_api):
    with pytest.raises(FailedWSLogin):
        mocked_ws_api.watchlist()


def test_positions_success(mocked_ws_api):
    mocked_ws_api.login('test01@gmail.com', 'blopblopblop', '789523')
    positions = mocked_ws_api.positions()

    assert isinstance(positions, list)
    assert len(positions) == 9
    assert all([isinstance(p, WSPosition) for p in positions])


def test_positions_not_logged(mocked_ws_api):
    with pytest.raises(FailedWSLogin):
        mocked_ws_api.positions()
