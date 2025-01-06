import sys
from types import ModuleType

from pgcrud.config import config
from pgcrud.db import ConnectionPool, Connection, Cursor, AsyncConnectionPool, AsyncConnection, AsyncCursor
from pgcrud.expressions import CurrentRow, Identifier, Literal, Undefined, Unbounded
from pgcrud.operations.get_one import get_one
from pgcrud.operations.get_many import get_many
from pgcrud.operations.insert_one import insert_one
from pgcrud.operations.insert_many import insert_many
from pgcrud.operations.update_many import update_many
from pgcrud.operations.delete_many import delete_many
from pgcrud.operations.async_get_one import async_get_one
from pgcrud.operations.async_get_many import async_get_many
from pgcrud.operations.async_insert_one import async_insert_one
from pgcrud.operations.async_insert_many import async_insert_many
from pgcrud.operations.async_update_many import async_update_many
from pgcrud.operations.async_delete_many import async_delete_many
from pgcrud.query_builder import QueryBuilder


__all__ = [
    'config',

    'ConnectionPool',
    'Connection',
    'Cursor',
    'AsyncConnectionPool',
    'AsyncConnection',
    'AsyncCursor',
    'connect',

    'QueryBuilder',

    'Identifier',
    'Literal',

    'UNDEFINED',
    'UNBOUNDED',
    'CURRENT_ROW',

    'get_one',
    'get_many',
    'insert_one',
    'insert_many',
    'update_many',
    'delete_many',

    'async_get_one',
    'async_get_many',
    'async_insert_one',
    'async_insert_many',
    'async_update_many',
    'async_delete_many',
]


connect = Connection.connect
UNDEFINED = Undefined()

UNBOUNDED: Unbounded
CURRENT_ROW: CurrentRow


class InitModule(ModuleType):

    @property
    def UNBOUNDED(self) -> Unbounded:
        return Unbounded()

    @property
    def CURRENT_ROW(self) -> CurrentRow:
        return CurrentRow()


sys.modules[__name__].__class__ = InitModule
