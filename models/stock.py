import dataclasses


SQL_SCHEMA = """
    CREATE TABLE IF NOT EXISTS stock (
        id BIGSERIAL,
        short_name VARCHAR(512),
        long_name VARCHAR(1024),
        
        symbol VARCHAR(16),
        sector VARCHAR(64),
        exchange VARCHAR(64),
        currency VARCHAR(16),
        timezone VARCHAR(128),
        
        price FLOAT,
        beta FLOAT,
        
        dividend_yield FLOAT,
        ex_dividend_data BIGINT,
        payout_ratio FLOAT,
        
        debt_equity_ratio FLOAT,
        monthly_return FLOAT,
        
        PRIMARY KEY (id)
    );
"""


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
