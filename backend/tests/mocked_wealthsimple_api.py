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
            Stock(id=2163580325505409658, ws_id='sec-s-3e036b4205684dd89faf37fe5b0e13af', name='National Bank Of Canada', type='equity', symbol='NA', sa_symbol='NA:CA', currency='CAD', exchange='TSX', price=92.17, can_use_fractional=True, buyable=True, eps=9.63947, pe=9.56172901622185, high52=104.83, low52=82.16, div_ex_date=1671667200, div_yield=0.0421, div_distribution='Quarterly'),
            Stock(id=3146122148577486529, ws_id='sec-s-62d0287aaad241749fcb3982c92509e4', name='Hamilton Enhanced U.S. Covered Call ETF - Canadian Hedged', type='exchange_traded_fund', symbol='HYLD', sa_symbol='HYLD:CA', currency='CAD', exchange='TSX', price=11.91, can_use_fractional=False, buyable=True, eps=None, pe=None, high52=17.27, low52=10.64, div_ex_date=1672272000, div_yield=0.11710000000000001, div_distribution='Monthly'),
            Stock(id=3402127093136367969, ws_id='sec-s-806428a6a78c4df7be22fc4bc014b5dd', name='Canoe EIT Income Fund', type='equity', symbol='EIT.UN', sa_symbol='EIT.UN:CA', currency='CAD', exchange='TSX', price=13.37, can_use_fractional=False, buyable=True, eps=None, pe=None, high52=13.82, low52=13.12, div_ex_date=1671580800, div_yield=0.0898, div_distribution='Monthly'),
            Stock(id=1018081011694051566, ws_id='sec-s-a01e4c0037344ff5a514e554258b552c', name='Labrador Iron Ore Royalty Corp', type='equity', symbol='LIF', sa_symbol='LIF:CA', currency='CAD', exchange='TSX', price=34.28, can_use_fractional=True, buyable=True, eps=4.26571, pe=8.03617686153067, high52=51.0, low52=25.24, div_ex_date=1672272000, div_yield=0.1036, div_distribution='Quarterly'),
            Stock(id=8736372625773831227, ws_id='sec-s-aee2d0052b904ee5bb08bf2f4e9f4983', name='Hamilton Enhanced Multi Sector Covered Call ETF Class E', type='exchange_traded_fund', symbol='HDIV', sa_symbol='HDIV:CA', currency='CAD', exchange='TSX', price=15.74, can_use_fractional=False, buyable=True, eps=None, pe=None, high52=19.39, low52=13.91, div_ex_date=1672272000, div_yield=0.0943, div_distribution='Monthly'),
            Stock(id=6166171216354714965, ws_id='sec-s-b34b6f1624234270b2862dc4f50e9b4c', name='Harvest Diversified Monthly Income ETF - Class A', type='exchange_traded_fund', symbol='HDIF', sa_symbol='HDIF:CA', currency='CAD', exchange='TSX', price=8.0, can_use_fractional=False, buyable=True, eps=None, pe=None, high52=10.35, low52=7.17, div_ex_date=1672272000, div_yield=0.0708, div_distribution='Monthly'),
            Stock(id=5263475689955598409, ws_id='sec-s-bc862eacf0b043acb7ff18c8107200aa', name='Global Dividend Growth Split Corp - Class A', type='equity', symbol='GDV', sa_symbol='GDV:CA', currency='CAD', exchange='TSX', price=10.71, can_use_fractional=False, buyable=True, eps=None, pe=None, high52=13.04, low52=9.23, div_ex_date=1672272000, div_yield=0.11199999999999999, div_distribution='Monthly'),
            Stock(id=6089422563498829543, ws_id='sec-s-cac48e23f5b84b4787b97628581ce59f', name='Bank of Nova Scotia', type='equity', symbol='BNS', sa_symbol='BNS:CA', currency='CAD', exchange='TSX', price=66.38, can_use_fractional=True, buyable=True, eps=8.32913, pe=7.96961987626559, high52=95.0, low52=63.19, div_ex_date=1672704000, div_yield=0.0621, div_distribution='Quarterly'),
            Stock(id=7952306825162794134, ws_id='sec-s-d4047f55ea8f46f698439b7b6c3e07d0', name='Barrick Gold Corp.', type='equity', symbol='ABX', sa_symbol='ABX:CA', currency='CAD', exchange='TSX', price=23.61, can_use_fractional=True, buyable=True, eps=1.106163312, pe=21.3440454441686, high52=33.016442, low52=17.822047, div_ex_date=1669680000, div_yield=0.0359, div_distribution='Quarterly'),
            Stock(id=5145473064763072867, ws_id='sec-s-e84cc1efee3447a5b9f21e6f47cc6799', name='BMO Canadian High Dividend Covered Call ETF', type='exchange_traded_fund', symbol='ZWC', sa_symbol='ZWC:CA', currency='CAD', exchange='TSX', price=17.26, can_use_fractional=True, buyable=True, eps=None, pe=None, high52=20.4, low52=16.2, div_ex_date=1672185600, div_yield=0.0691, div_distribution='Monthly')
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
