from abc import ABC, abstractmethod
from typing import List

from backend.models.ws_account import WSAccount
from backend.models.ws_position import WSPosition
from backend.models.stock import Stock
from backend.models.ws_token_set import WSTokenSet
from backend.models.ws_user import WSUser
from backend.models.activity import Activity


class FailedWSLogin(BaseException):
    pass


class IWealthSimpleAPI(ABC):
    @abstractmethod
    def login(self, username: str, password: str, otp: str) -> WSTokenSet:
        pass

    @abstractmethod
    def refresh(self, refresh_token: str) -> WSTokenSet:
        pass

    @abstractmethod
    def me(self) -> WSUser:
        pass

    @abstractmethod
    def accounts(self) -> List[WSAccount]:
        pass

    @abstractmethod
    def positions(self) -> List[WSPosition]:
        pass

    @abstractmethod
    def activities(self) -> List[Activity]:
        pass

    @abstractmethod
    def watchlist(self) -> List[Stock]:
        pass
