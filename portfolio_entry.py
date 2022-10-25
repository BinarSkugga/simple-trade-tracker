import dataclasses


@dataclasses.dataclass
class PortfolioEntry:
    id: int
    portfolio_id: int
    stock_id: int
    count: int
    date: int
