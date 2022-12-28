import dataclasses

SQL_SCHEMA = """
    CREATE TABLE IF NOT EXISTS stock (
        id BIGSERIAL,
        ws_id VARCHAR(256),
        name VARCHAR(1024),

        type VARCHAR(32),
        symbol VARCHAR(16),
        sa_symbol VARCHAR(16),
        currency VARCHAR(16),
        exchange VARCHAR(64),

        price FLOAT,

        can_use_fractional BOOLEAN,
        buyable BOOLEAN,
        limited BOOLEAN,

        eps FLOAT,
        pe FLOAT,
        high52 FLOAT,
        low52 FLOAT,

        div_ex_date BIGINT,
        div_yield FLOAT,
        div_distribution VARCHAR(24),

        PRIMARY KEY (id)
    );
"""


@dataclasses.dataclass
class Stock:
    id: int
    ws_id: str
    name: str

    type: str
    symbol: str
    sa_symbol: str
    currency: str
    exchange: str

    price: float

    can_use_fractional: bool
    buyable: bool
    limited: bool = False

    eps: float = None
    pe: float = None
    high52: float = None
    low52: float = None

    div_ex_date: int = None
    div_yield: float = None
    div_distribution: str = None
