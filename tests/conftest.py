import os

from pytest import fixture

import pgcrud as pg


__all__ = [
    'conn',
    'cursor',
]


@fixture(scope='session')
def conn():
    conn_str = os.environ['CONN_STR']
    with pg.connect(conn_str) as conn:
        yield conn


@fixture
def cursor(conn: pg.Connection):
    with conn.cursor() as cursor:
        cursor.execute("SET search_path = test_schema")
        yield cursor


def pytest_sessionstart():

    conn_str = os.environ['CONN_STR']
    with pg.connect(conn_str) as conn:
        with conn.cursor() as cursor:
            cursor.execute("DROP SCHEMA IF EXISTS test_schema CASCADE")
            cursor.execute("CREATE SCHEMA test_schema")
            cursor.execute("SET search_path = test_schema")

            with open('setup_schema.sql', 'r') as f:
                for query in f.read().split(';'):
                    cursor.execute(query)   # type: ignore


# def pytest_sessionfinish(session):
#
#     conn_str = os.environ['CONN_STR']
#     with psycopg.connect(conn_str) as conn:
#         with conn.cursor() as cursor:
#             cursor.execute("DROP SCHEMA IF EXISTS demo_schema CASCADE")
