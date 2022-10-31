import dataclasses


SQL_SCHEMA = """
    CREATE TABLE IF NOT EXISTS portfolio_entry (
        id BIGSERIAL,
        portfolio_id BIGINT,
        stock_id BIGINT,
        count INTEGER,
        strike FLOAT,
        date BIGINT,

        PRIMARY KEY (id),
        CONSTRAINT fk_portfolio
          FOREIGN KEY(portfolio_id) 
          REFERENCES portfolio(id),
        CONSTRAINT fk_stock
          FOREIGN KEY(stock_id) 
          REFERENCES stock(id)
    );
"""


@dataclasses.dataclass
class PortfolioEntry:
    id: int
    portfolio_id: int
    stock_id: int
    count: int
    strike: float
    date: int
