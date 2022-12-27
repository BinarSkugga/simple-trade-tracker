import os
import traceback
import uuid
from typing import Union
import psycopg
from psycopg import DatabaseError
from psycopg.errors import DuplicateDatabase, InvalidCatalogName
from psycopg.sql import Composed

POSTGRES_URI = os.environ['DATABASE_URL']


def generate_id() -> int:
    return uuid.uuid4().int >> (128 - 63)


def execute(query: Union[Composed, str], connection_uri: str = POSTGRES_URI, fetch: bool = True, autocommit: bool = False):
    with psycopg.connect(connection_uri) as connection:
        connection.autocommit = autocommit
        with connection.cursor() as cursor:
            cursor.execute(query)

            if fetch:
                return cursor.fetchall()
            connection.commit()


def execute_gen(query: Union[Composed, str], connection_uri: str = POSTGRES_URI,):
    with psycopg.connect(connection_uri) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(query)

                for record in cursor:
                    yield record

                connection.commit()
            except DatabaseError:
                traceback.print_exc()


def create_database(database_name: str) -> None:
    connection_uri = POSTGRES_URI.rsplit('/', 1)
    connection_uri[1] = 'postgres'
    connection_uri = ','.join(connection_uri)

    try:
        execute(f"CREATE DATABASE {database_name};", connection_uri=connection_uri, fetch=False, autocommit=True)
    except DuplicateDatabase:
        pass


def drop_database(database_name: str) -> None:
    connection_uri = POSTGRES_URI.rsplit('/', 1)
    connection_uri[1] = 'postgres'
    connection_uri = '/'.join(connection_uri)

    version = execute('SHOW server_version;', connection_uri=connection_uri)[0][0].split(' ')[0]
    major = int(version.split('.')[0])

    try:
        if major >= 13:
            execute(f"DROP DATABASE {database_name} WITH (FORCE);",
                    autocommit=True, fetch=False, connection_uri=connection_uri)
        else:
            # Prevent new connections and terminate all current ones
            execute(
                f"UPDATE pg_database SET datallowconn = false WHERE datname = '{database_name}';",
                fetch=False, connection_uri=connection_uri
            )
            execute(f"""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = '{database_name}';
            """, fetch=False, connection_uri=connection_uri)

            # Drop database
            execute(f"DROP DATABASE {database_name};", fetch=False, autocommit=True, connection_uri=connection_uri)
    except InvalidCatalogName:
        pass
