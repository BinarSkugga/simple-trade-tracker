import time
from typing import List, Optional

from interface.wealthsimple_api_interface import IWealthSimpleAPI, FailedWSLogin
from models.ws_account import WSAccount
from models.ws_position import WSPosition
from models.stock import Stock
from models.ws_token_set import WSTokenSet
from models.ws_user import WSUser


class MockedWealthSimpleAPI(IWealthSimpleAPI):
    seed: dict = {
        'users': [
            WSUser(canonical_id='user-07b3b5bc-f36e-4c80-8dc2-a02061f406c4', first_name='Roger', last_name='Smith', email='test01@gmail.com'),
            WSUser(canonical_id='user-46415747-8fc2-4328-bc8f-8318a089c64f', first_name='Henry', last_name='Tremblay', email='test02@gmail.com'),
            WSUser(canonical_id='user-381915d1-6ae6-4ac5-825f-5c658a8a3e56', first_name='Bertrand', last_name='Lamouille', email='test03@gmail.com'),
        ],

        'stocks': [
            Stock(id=9162481200008143540, ws_id='sec-s-3e036b4205684dd89faf37fe5b0e13af', name='National Bank Of Canada', type='equity', symbol='NA', sv_symbol='NA:CA', currency='CAD', exchange='TSX', price=92.17, can_use_fractional=True, buyable=True, eps=9.7374, pe=9.47, beta=1.1517, high52=104.83, low52=82.16, ex_dividend_date=1663891200, dividend_yield=0.0494),
            Stock(id=8096130168390492833, ws_id='sec-s-62d0287aaad241749fcb3982c92509e4', name='Hamilton Enhanced U.S. Covered Call ETF - Canadian Hedged', type='exchange_traded_fund', symbol='HYLD', currency='CAD', exchange='TSX', price=11.91, can_use_fractional=False, buyable=True, eps=None, pe=None, beta=1.617, high52=17.27, low52=10.64, ex_dividend_date=None, dividend_yield=0.1171),
            Stock(id=1928698703642960138, ws_id='sec-s-806428a6a78c4df7be22fc4bc014b5dd', name='Canoe EIT Income Fund', type='equity', symbol='EIT.UN', currency='CAD', exchange='TSX', price=13.37, can_use_fractional=False, buyable=True, eps=1.6158, pe=8.27, beta=1.0682, high52=14.89, low52=12.04, ex_dividend_date=None, dividend_yield=0.0898),
            Stock(id=2229126502340896008, ws_id='sec-s-a01e4c0037344ff5a514e554258b552c', name='Labrador Iron Ore Royalty Corp', type='equity', symbol='LIF', currency='CAD', exchange='TSX', price=34.28, can_use_fractional=True, buyable=True, eps=4.673, pe=7.34, beta=1.0549, high52=51, low52=25.24, ex_dividend_date=1664323200, dividend_yield=0.1036),
            Stock(id=7350766160146080051, ws_id='sec-s-aee2d0052b904ee5bb08bf2f4e9f4983', name='Hamilton Enhanced Multi Sector Covered Call ETF Class E', type='exchange_traded_fund', symbol='HDIV', currency='CAD', exchange='TSX', price=15.74, can_use_fractional=False, buyable=True, eps=None, pe=None, beta=1.45, high52=19.39, low52=13.91, ex_dividend_date=None, dividend_yield=0.0943),
            Stock(id=1561780008406852115, ws_id='sec-s-b34b6f1624234270b2862dc4f50e9b4c', name='Harvest Diversified Monthly Income ETF - Class A', type='exchange_traded_fund', symbol='HDIF', currency='CAD', exchange='TSX', price=8.0, can_use_fractional=False, buyable=True, eps=None, pe=None, beta=0.9963, high52=10.35, low52=7.16, ex_dividend_date=None, dividend_yield=0.0708),
            Stock(id=6255349601691837577, ws_id='sec-s-bc862eacf0b043acb7ff18c8107200aa', name='Global Dividend Growth Split Corp - Class A', type='equity', symbol='GDV', currency='CAD', exchange='TSX', price=10.71, can_use_fractional=False, buyable=True, eps=None, pe=None, beta=1.1644, high52=13.04, low52=9.23, ex_dividend_date=None, dividend_yield=0.112),
            Stock(id=4467138413975970390, ws_id='sec-s-cac48e23f5b84b4787b97628581ce59f', name='Bank of Nova Scotia', type='equity', symbol='BNS', currency='CAD', exchange='TSX', price=66.38, can_use_fractional=True, buyable=True, eps=8.0484, pe=8.25, beta=1.0024, high52=95, low52=63.19, ex_dividend_date=1664755200, dividend_yield=0.0612),
            Stock(id=3156432814975853192, ws_id='sec-s-d4047f55ea8f46f698439b7b6c3e07d0', name='Barrick Gold Corp.', type='equity', symbol='ABX', currency='CAD', exchange='TSX', price=23.61, can_use_fractional=True, buyable=True, eps=None, pe=None, beta=0.4651, high52=33.0164, low52=17.822, ex_dividend_date=None, dividend_yield=0.0356),
            Stock(id=1375778513932822493, ws_id='sec-s-e84cc1efee3447a5b9f21e6f47cc6799', name='BMO Canadian High Dividend Covered Call ETF', type='exchange_traded_fund', symbol='ZWC', currency='CAD', exchange='TSX', price=17.36, can_use_fractional=True, buyable=True, eps=None, pe=11.265, beta=0.9969, high52=20.4, low52=16.15, ex_dividend_date=1604966400, dividend_yield=0.0691)
        ],

        'positions': [
            WSPosition(id=5802196904218698598, ws_id='sec-s-d4047f55ea8f46f698439b7b6c3e07d0', quantity=6.918, sellable_quantity=6.918, book_value=153.27, market_value=163.33398),
            WSPosition(id=2324805000825151768, ws_id='sec-s-cac48e23f5b84b4787b97628581ce59f', quantity=4, sellable_quantity=4, book_value=271.13, market_value=265.52),
            WSPosition(id=426675089348665452, ws_id='sec-s-806428a6a78c4df7be22fc4bc014b5dd', quantity=13, sellable_quantity=13, book_value=177.57, market_value=173.81),
            WSPosition(id=7739044506639574959, ws_id='sec-s-bc862eacf0b043acb7ff18c8107200aa', quantity=20, sellable_quantity=20, book_value=211.66, market_value=214.20000000000002),
            WSPosition(id=1299559887320589834, ws_id='sec-s-b34b6f1624234270b2862dc4f50e9b4c', quantity=17, sellable_quantity=17, book_value=141.21, market_value=136.0),
            WSPosition(id=4495415683580798106, ws_id='sec-s-62d0287aaad241749fcb3982c92509e4', quantity=40, sellable_quantity=40, book_value=488.15, market_value=476.4),
            WSPosition(id=2560764236839167627, ws_id='sec-s-a01e4c0037344ff5a514e554258b552c', quantity=4.9983, sellable_quantity=4.9983, book_value=159.75, market_value=171.34172400000003),
            WSPosition(id=6559539882678167140, ws_id='sec-s-3e036b4205684dd89faf37fe5b0e13af', quantity=2, sellable_quantity=2, book_value=192.77, market_value=184.34),
            WSPosition(id=7993973712664077190, ws_id='sec-s-e84cc1efee3447a5b9f21e6f47cc6799', quantity=15, sellable_quantity=15, book_value=266.25, market_value=260.4)
        ]
    }

    def __init__(self, expiry: int = 60):
        self.logged_in: Optional[WSUser] = None
        self.token_set: Optional[WSTokenSet] = None
        self.expiry = expiry

    def _validate_token_set(self):
        if self.logged_in is None or self.token_set is None:
            raise FailedWSLogin()
        if self.token_set.expire < time.time():
            raise FailedWSLogin()

    def login(self, username: str, password: str, otp: str) -> WSTokenSet:
        # Fake the entire login process because I can't really mock it reliably
        user = next(iter(u for u in self.seed['users'] if u.email == username), None)
        if user is None:
            raise FailedWSLogin()
        if password != 'blopblopblop':
            raise FailedWSLogin()
        if otp != '789523':
            raise FailedWSLogin()

        self.logged_in = user
        self.token_set = WSTokenSet(
            access='master_access',
            refresh='master_refresh',
            expire=int(time.time() + self.expiry)
        )
        return self.token_set

    def refresh(self, refresh_token: str) -> WSTokenSet:
        if refresh_token != 'master_refresh':
            raise FailedWSLogin()
        self._validate_token_set()

        return WSTokenSet(
            access='master_access',
            refresh='master_refresh',
            expire=int(time.time() + self.expiry)
        )

    def me(self) -> WSUser:
        self._validate_token_set()

        return self.logged_in

    def accounts(self) -> List[WSAccount]:
        pass

    def positions(self) -> List[WSPosition]:
        self._validate_token_set()

        return self.seed['positions']

    def watchlist(self) -> List[Stock]:
        self._validate_token_set()

        return self.seed['stocks']
