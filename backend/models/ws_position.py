import dataclasses

SQL_SCHEMA = """
    CREATE TABLE IF NOT EXISTS "position" (
        id BIGSERIAL,
        ws_id VARCHAR(256),
        
        quantity FLOAT,
        sellable_quantity FLOAT,
        book_value FLOAT,
        market_value FLOAT,

        PRIMARY KEY (id)
    );
"""


@dataclasses.dataclass
class WSPosition:
    id: int
    ws_id: str

    quantity: float
    sellable_quantity: float
    book_value: float
    market_value: float
