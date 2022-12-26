import os
import time
from datetime import datetime
from typing import List

import requests
from pyotp import TOTP

from models.ws_account import WSAccount
from models.ws_position import WSPosition
from models.ws_stock import WSStock
from models.ws_token_keyring import WSTokenKeyring
from models.ws_user import WSUser

WS_HOST = 'https://trade-service.wealthsimple.com'


def iso_to_epoch(iso: str) -> int:
    if iso is None:
        return None
    utc_time = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ")
    return int((utc_time - datetime(1970, 1, 1)).total_seconds())


def ws_login(username: str, password: str, otp: str) -> WSTokenKeyring:
    response = requests.post(f'{WS_HOST}/auth/login', json={
        'email': username,
        'password': password,
        'otp': otp
    })

    if response.status_code != 200:
        raise ValueError(response.json())

    return WSTokenKeyring(**{
        'access': response.headers.get('X-Access-Token'),
        'refresh': response.headers.get('X-Refresh-Token'),
        'expire': int(response.headers.get('X-Access-Token-Expires'))
    })


def ws_refresh(refresh_token: str) -> WSTokenKeyring:
    response = requests.post(f'{WS_HOST}/auth/refresh', json={
        'refresh_token': refresh_token
    })

    if response.headers.get('X-Access-Token-Expires') is None:
        os.remove('refresh.txt')
        return None

    return WSTokenKeyring(**{
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
        'id': position['id'],
        'currency': position['currency'],
        'symbol': position['stock']['symbol'],
        'name': position['stock']['name'],
        'exchange': position['stock']['primary_exchange'],
        'type': position['security_type'],

        'quantity': position['quantity'],
        'sellable_quantity': position['sellable_quantity'],
        'book_value': position['book_value']['amount'],
        'market_value': float(position['quote']['amount']) * position['quantity'],

        'available': position['ws_trade_eligible'],
        'buyable': position['buyable'],
        'active': position['active'],
        'volatile': position['is_volatile']
    }) for position in body['results']]


def ws_watchlist(access_token: str, account_id: str) -> List[WSStock]:
    response = requests.get(f'{WS_HOST}/watchlist', params={'account_id': account_id},
                            headers={'Authorization': access_token})
    body = response.json()
    simple_stocks = [WSStock(**{
        'id': None,
        'ws_id': stock['id'],
        'name': stock['stock']['name'],

        'type': stock['security_type'],
        'symbol': stock['stock']['symbol'],
        'currency': stock['currency'],
        'exchange': stock['stock']['primary_exchange'],

        'price': float(stock['quote']['amount']),

        'can_use_fractional': 'fractional' in stock['allowed_order_subtypes'],
        'buyable': stock['buyable']
    }) for stock in body['securities']]

    for stock in simple_stocks:
        response = requests.get(f'{WS_HOST}/securities/{stock.ws_id}',
                                headers={'Authorization': access_token})
        body = response.json()
        stock.eps = body['fundamentals']['eps']
        stock.pe = body['fundamentals']['pe_ratio']
        stock.beta = body['fundamentals']['beta']
        stock.high52 = body['fundamentals']['high_52_week']
        stock.low52 = body['fundamentals']['low_52_week']
        stock.ex_dividend_date = iso_to_epoch(body['fundamentals']['ex_div_date'])
        stock.dividend_yield = body['fundamentals']['yield']

    return simple_stocks


def ws_security_info(access_token: str, security_id: str) -> dict:
    response = requests.get(f'{WS_HOST}/securities/{security_id}', headers={'Authorization': access_token})
    body = response.json()
    return body


class WealthSimpleAPI:
    def __init__(self, email: str, password: str, otp_secret: str):
        self.email = email
        self.totp = TOTP(otp_secret)
        self.email = email
        self.password = password
        self.account_id = None
        self.account = None

        if not os.path.exists('refresh.txt'):
            self.key_ring = ws_login(email, password, self.totp.now())
            with open('refresh.txt', 'w') as f:
                f.write(self.key_ring.refresh)
        else:
            with open('refresh.txt', 'r') as f:
                self.key_ring = WSTokenKeyring(access='', refresh=f.readline(), expire=0)
            self.auto_refresh()

    def set_account(self, account_id: str):
        self.account_id = account_id
        self.account = next((account for account in self.accounts() if account.id == account_id), None)
        print(f'Account selected: {self.account.id}')

    def refresh(self):
        key_ring = ws_refresh(self.key_ring.refresh)

        if key_ring is None:
            self.key_ring = ws_login(self.email, self.password, self.totp.now())
        else:
            self.key_ring = ws_refresh(self.key_ring.refresh)

    def auto_refresh(self):
        if self.key_ring.expire <= time.time():
            self.refresh()

    def me(self) -> WSUser:
        self.auto_refresh()
        return ws_me(self.key_ring.access)

    def accounts(self):
        self.auto_refresh()
        return ws_accounts(self.key_ring.access)

    def positions(self):
        self.auto_refresh()
        return ws_positions(self.key_ring.access, self.account.id)

    def watchlist(self):
        self.auto_refresh()
        return ws_watchlist(self.key_ring.access, self.account.id)

    def security_info(self, security_id: str):
        self.auto_refresh()
        return ws_security_info(self.key_ring.access, security_id)
