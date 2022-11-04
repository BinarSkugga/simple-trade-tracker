import dataclasses
from typing import Dict


@dataclasses.dataclass
class WSAccount:
    id: str
    currency: str
    type: str
    available_balance: float
    securities: Dict[str, int]
