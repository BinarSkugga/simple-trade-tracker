import dataclasses
from typing import Union, Any

from psycopg.sql import SQL, Identifier, Literal, Composed

from database_utils import execute, execute_gen

SQL_LIST = 'SELECT * FROM {table}'
SQL_FIND = 'SELECT * FROM {table} {filters}'
SQL_INSERT = 'INSERT INTO {table} {columns} VALUES {values} RETURNING *'
SQL_DELETE_FILTERED = 'DELETE FROM {table} {filters}'
SQL_UPDATE = 'UPDATE {table} SET {update_set} WHERE "id"={id}'
SQL_UPSERT = "INSERT INTO {table} {columns} VALUES {values} " \
             "ON CONFLICT {conflict_columns} DO UPDATE SET {update_set} RETURNING *"


def dict_to_sql_columns(data: dict):
    return SQL('(') + SQL(',').join([Identifier(key) for key in data.keys()]) + SQL(')')


def dict_to_sql_values(data: Union[list, dict]):
    if isinstance(data, list):
        return SQL(',').join([dict_to_sql_values(d) for d in data])
    return SQL('(') + SQL(',').join([
        Literal(value) if not isinstance(value, Composed) else value
        for value in data.values()
    ]) + SQL(')')


def dict_to_sql_set(data: dict, use_excluded: bool = False):
    set_ = []
    for key, value in data.items():
        val = Literal(value) if not isinstance(value, Composed) else value
        entry = Identifier(key) + SQL('=') + (SQL('EXCLUDED.' + key) if use_excluded else val)
        set_.append(entry)
    return SQL(',').join(set_)


class Repository:
    def __init__(self, table_name: str, model_class):
        self.table_name = table_name
        self.model_class = model_class

        self.fields = {f.name: f for f in dataclasses.fields(model_class)}

    def list(self):
        return execute_gen(SQL(SQL_LIST).format(
            table=Identifier(self.table_name),
        ))

    def get(self, id: int):
        return next(self.find('id', id), None)

    def find(self, column: str, value: Any):
        records = execute_gen(SQL(SQL_FIND).format(
            table=Identifier(self.table_name),
            filters=SQL('WHERE {column}={value}').format(column=Identifier(column), value=Literal(value))
        ))

        for record in records:
            yield self.model_class(*record)

    def upsert(self, entity):
        data = dataclasses.asdict(entity)
        if entity.id == 0:
            entity.id = 'DEFAULT'

        execute(SQL(SQL_UPSERT).format(
            table=Identifier(self.table_name),
            columns=dict_to_sql_columns(data),
            values=dict_to_sql_values(data),
            update_set=dict_to_sql_set(data, use_excluded=True),
            conflict_columns=dict_to_sql_columns({'id': None})
        ), False)
