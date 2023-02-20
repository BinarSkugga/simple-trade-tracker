import dataclasses

SQL_SCHEMA = """
    CREATE TABLE IF NOT EXISTS "activity" (
        id BIGSERIAL,
        type VARCHAR(32),
        date BIGINT,
        
        amount FLOAT,
        currency VARCHAR(16),
        
        symbol VARCHAR(32),
        status VARCHAR(32),
        quantity INTEGER,
        security_id VARCHAR(256),
        limit_price FLOAT,
        order_type VARCHAR(32),
        order_sub_type VARCHAR(32),
        
        PRIMARY KEY (id)
    );
"""


@dataclasses.dataclass
class Activity:
    id: int
    type: str
    date: int

    amount: float
    currency: str

    symbol: str = None
    status: str = None
    quantity: int = None
    security_id: str = None
    limit_price: float = None
    order_type: str = None
    order_sub_type: str = None
