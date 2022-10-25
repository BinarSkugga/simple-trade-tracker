import os
import traceback
from typing import Union
import psycopg
from psycopg import DatabaseError
from psycopg.sql import Composed

POSTGRES_URI = os.environ['DATABASE_URL']


def execute(query: Union[Composed, str], fetch: bool = True):
    with psycopg.connect(POSTGRES_URI) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(query)

                if fetch:
                    return cursor.fetchall()
                connection.commit()
            except DatabaseError as _:
                traceback.print_exc()


def execute_gen(query: Union[Composed, str]):
    with psycopg.connect(POSTGRES_URI) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(query)

                for record in cursor:
                    yield record

                connection.commit()
            except DatabaseError as _:
                traceback.print_exc()
