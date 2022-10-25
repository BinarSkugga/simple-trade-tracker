import dataclasses
from typing import List

from portfolio_entry import PortfolioEntry


@dataclasses.dataclass
class Portfolio:
    id: int
    name: str
    owner: int

    entries: List[PortfolioEntry] = None
