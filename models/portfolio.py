import dataclasses
from typing import List

from models.portfolio_entry import PortfolioEntry

SQL_SCHEMA = """
    CREATE TABLE IF NOT EXISTS portfolio (
        id BIGSERIAL,
        name VARCHAR(128),
        user_id BIGINT,

        PRIMARY KEY (id),
        CONSTRAINT fk_user
          FOREIGN KEY(user_id) 
          REFERENCES "user"(id)
    );
"""


@dataclasses.dataclass
class Portfolio:
    id: int
    name: str
    user_id: int

    entries: List[PortfolioEntry] = None


def portfolio_dumper(model_class, entity):
    data = dataclasses.asdict(entity)
    if 'entries' in data:
        data.pop('entries')
    return data
