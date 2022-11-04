import os
import time
from typing import List

import requests
from pyotp import TOTP

from models.ws_account import WSAccount
from models.ws_position import WSPosition
from models.ws_token_keyring import WSTokenKeyring
from models.ws_user import WSUser

WS_HOST = 'https://trade-service.wealthsimple.com'


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
        'email': body['email'],
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


class WealthSimpleAPI:
    def __init__(self, email: str, password: str, otp_secret: str):
        self.email = email
        self.totp = TOTP(otp_secret)
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

    def refresh(self):
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
