import dataclasses

SQL_SCHEMA = """
    CREATE TABLE IF NOT EXISTS "user" (
        id BIGSERIAL,
        username VARCHAR(256),
        password_hash VARCHAR(512),
        role VARCHAR(32),

        PRIMARY KEY (id)
    );
"""


@dataclasses.dataclass
class User:
    id: int
    username: str
    password_hash: str
    role: str = 'default'
