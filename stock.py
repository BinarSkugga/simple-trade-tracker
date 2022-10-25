import dataclasses


@dataclasses.dataclass()
class Stock:
    id: int
    short_name: str
    long_name: str

    symbol: str
    sector: str
    exchange: str
    timezone: str
    currency: str

    price: float
    beta: float  # lower than 2

    dividend_yield: float  # as high as possible
    ex_dividend_date: int
    payout_ratio: float  # between 0.3 to 0.5

    debt_equity_ratio: float  # lower than 2
    # growth_estimate_5y: float  # between 0.05 and 0.15

    monthly_return: float = 0.0
