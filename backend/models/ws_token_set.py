import dataclasses


@dataclasses.dataclass
class WSTokenSet:
    access: str
    refresh: str
    expire: int
