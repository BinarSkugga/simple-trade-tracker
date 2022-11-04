import dataclasses


@dataclasses.dataclass
class WSPosition:
    id: str
    currency: str
    symbol: str
    name: str
    exchange: str
    type: str

    quantity: float
    sellable_quantity: float
    book_value: float
    market_value: float

    available: bool
    buyable: bool
    active: bool
    volatile: bool
