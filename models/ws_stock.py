import dataclasses

SQL_SCHEMA = """
    CREATE TABLE IF NOT EXISTS stock (
        id BIGSERIAL,
        ws_id VARCHAR(256),
        name VARCHAR(1024),

        type VARCHAR(32),
        symbol VARCHAR(16),
        currency VARCHAR(16),
        exchange VARCHAR(64),

        price FLOAT,

        can_use_fractional BOOLEAN,
        buyable BOOLEAN,
        
        eps FLOAT,
        pe FLOAT,
        beta FLOAT,
        high52 FLOAT,
        low52 FLOAT,
        ex_dividend_date BIGINT,
        dividend_yield FLOAT,

        PRIMARY KEY (id)
    );
"""


@dataclasses.dataclass
class WSStock:
    id: int
    ws_id: str
    name: str

    type: str
    symbol: str
    currency: str
    exchange: str

    price: float

    can_use_fractional: bool
    buyable: bool

    eps: float = None
    pe: float = None
    beta: float = None
    high52: float = None
    low52: float = None
    ex_dividend_date: int = None
    dividend_yield: float = None
