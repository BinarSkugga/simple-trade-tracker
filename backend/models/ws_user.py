import dataclasses


@dataclasses.dataclass
class WSUser:
    canonical_id: str
    first_name: str
    last_name: str
    email: str
