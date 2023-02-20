import os
import time
from typing import List

import requests
from pyotp import TOTP

from backend.config import WS_HOST, ACTIVITY_START
from backend.seeking_alpha_api import get_stock_symbol, get_stocks_info
from backend.interface.wealthsimple_api_interface import IWealthSimpleAPI
from backend.models.ws_account import WSAccount
from backend.models.ws_position import WSPosition
from backend.models.stock import Stock
from backend.models.ws_token_set import WSTokenSet
from backend.models.ws_user import WSUser
from backend.utils import iso_to_epoch, build_activity, get_activity_date
from models.activity import Activity


def ws_login(username: str, password: str, otp: str) -> WSTokenSet:
    response = requests.post(f'{WS_HOST}/auth/login', json={
        'email': username,
        'password': password,
        'otp': otp
    })

    if response.status_code != 200:
        raise ValueError(response.json())

    return WSTokenSet(**{
        'access': response.headers.get('X-Access-Token'),
        'refresh': response.headers.get('X-Refresh-Token'),
        'expire': int(response.headers.get('X-Access-Token-Expires'))
    })


def ws_refresh(refresh_token: str) -> WSTokenSet:
    response = requests.post(f'{WS_HOST}/auth/refresh', json={
        'refresh_token': refresh_token
    })

    if response.headers.get('X-Access-Token-Expires') is None:
        os.remove('refresh.txt')
        return None

    return WSTokenSet(**{
        'access': response.headers.get('X-Access-Token'),
        'refresh': response.headers.get('X-Refresh-Token'),
        'expire': int(response.headers.get('X-Access-Token-Expires'))
    })


def ws_me(access_token: str) -> WSUser:
    response = requests.get(f'{WS_HOST}/me', headers={'Authorization': access_token})
    body = response.json()
    return WSUser(**{
        'first_name': body['first_name'],
        'last_name': body['last_name'],
        'canonical_id': body['canonical_id'],
        'email': body['email']
    })


def ws_accounts(access_token: str) -> List[WSAccount]:
    response = requests.get(f'{WS_HOST}/account/list', headers={'Authorization': access_token})
    body = response.json()
    return [WSAccount(**{
        'id': account['id'],
        'currency': account['base_currency'],
        'type': account['account_type'],
        'available_balance': account['current_balance']['amount'],
        'securities': account['position_quantities']
    }) for account in body['results'] if 'tfsa' in account['account_type']]


def ws_positions(access_token: str, account_id: str) -> List[WSPosition]:
    response = requests.get(f'{WS_HOST}/account/positions', params={'account_id': account_id},
                            headers={'Authorization': access_token})
    body = response.json()
    return [WSPosition(**{
        'id': None,
        'ws_id': position['id'],

        'quantity': position['quantity'],
        'sellable_quantity': position['sellable_quantity'],
        'book_value': position['book_value']['amount'],
        'market_value': float(position['quote']['amount']) * position['quantity']
    }) for position in body['results']]


def ws_watchlist(access_token: str, account_id: str) -> List[Stock]:
    response = requests.get(f'{WS_HOST}/watchlist', params={'account_id': account_id},
                            headers={'Authorization': access_token})
    body = response.json()
    simple_stocks = [Stock(**{
        'id': None,
        'ws_id': stock['id'],
        'name': stock['stock']['name'],

        'type': stock['security_type'],
        'symbol': stock['stock']['symbol'],
        'sa_symbol': get_stock_symbol(stock['stock']['symbol'], stock['stock']['primary_exchange']),
        'currency': stock['currency'],
        'exchange': stock['stock']['primary_exchange'],

        'price': float(stock['quote']['amount']),

        'can_use_fractional': 'fractional' in stock['allowed_order_subtypes'],
        'buyable': stock['buyable']
    }) for stock in body['securities']]

    sa_symbols = [stock.sa_symbol for stock in simple_stocks]
    additional_info = get_stocks_info(sa_symbols)
    for stock in simple_stocks:
        details = next(iter(detail for detail in additional_info if detail['id'] == stock.sa_symbol), None)['attributes']
        if details['companyName'] is None:
            stock.limited = True
            continue

        stock.limited = False
        stock.eps = details['estimateEps']
        stock.pe = details['peRatioFwd']
        stock.high52 = details['high52']
        stock.low52 = details['low52']
        stock.div_ex_date = iso_to_epoch(details['dividends'][0]['exDate'])
        stock.div_yield = details['divYield'] / 100
        stock.div_distribution = details['divDistribution']

    return simple_stocks


def ws_activity(access_token: str, account_id: str, limit: int = 20) -> List[Activity]:
    json_activities = []
    bookmark = None

    activities_date = lambda: (get_activity_date(a) for a in json_activities if get_activity_date(a) != -1)
    while min(activities_date(), default=9999999999) >= ACTIVITY_START:
        params = {'account_id': account_id, 'limit': limit}
        if bookmark is not None:
            params['bookmark'] = bookmark

        response = requests.get(f'{WS_HOST}/account/activities', params=params, headers={'Authorization': access_token})
        data = response.json()
        bookmark = data['bookmark']
        json_activities += response.json()['results']

    activities = []
    for activity in json_activities:
        built = build_activity(activity)
        if built is not None:
            activities.append(build_activity(activity))

    return activities


def ws_security_info(access_token: str, security_id: str) -> dict:
    response = requests.get(f'{WS_HOST}/securities/{security_id}', headers={'Authorization': access_token})
    body = response.json()
    return body


class WealthSimpleAPI(IWealthSimpleAPI):
    def __init__(self, email: str, password: str, otp_secret: str):
        self.email = email
        self.totp = TOTP(otp_secret)
        self.email = email
        self.password = password
        self.account_id = None
        self.account = None

        if not os.path.exists('refresh.txt'):
            self.login(email, password, self.totp.now())
        else:
            with open('refresh.txt', 'r') as f:
                self.key_ring = WSTokenSet(access='', refresh=f.readline(), expire=0)
            self.refresh(self.key_ring.refresh)

    def set_account(self, account_id: str):
        self.account_id = account_id
        self.account = next((account for account in self.accounts() if account.id == account_id), None)
        print(f'Account selected: {self.account.id}')

    def login(self, username: str, password: str, otp: str) -> WSTokenSet:
        self.key_ring = ws_login(username, password, self.totp.now())
        with open('refresh.txt', 'w') as f:
            f.write(self.key_ring.refresh)

        return self.key_ring

    def refresh(self, refresh_token: str) -> WSTokenSet:
        if self.key_ring.expire <= time.time():
            key_ring = ws_refresh(refresh_token)

            if key_ring is None:
                self.key_ring = ws_login(self.email, self.password, self.totp.now())
            else:
                self.key_ring = ws_refresh(self.key_ring.refresh)

            with open('refresh.txt', 'w') as f:
                f.write(self.key_ring.refresh)

        return self.key_ring

    def me(self) -> WSUser:
        self.refresh(self.key_ring.refresh)
        return ws_me(self.key_ring.access)

    def accounts(self):
        self.refresh(self.key_ring.refresh)
        return ws_accounts(self.key_ring.access)

    def positions(self):
        self.refresh(self.key_ring.refresh)
        return ws_positions(self.key_ring.access, self.account.id)

    def watchlist(self):
        self.refresh(self.key_ring.refresh)
        return ws_watchlist(self.key_ring.access, self.account.id)

    def activity(self):
        self.refresh(self.key_ring.refresh)
        return ws_activity(self.key_ring.access, self.account.id)

    def security_info(self, security_id: str):
        self.refresh(self.key_ring.refresh)
        return ws_security_info(self.key_ring.access, security_id)
