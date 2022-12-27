import dataclasses


@dataclasses.dataclass
class WSTokenKeyring:
    access: str
    refresh: str
    expire: int
