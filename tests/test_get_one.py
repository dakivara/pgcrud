import pgcrud as pg
from pgcrud import e

from tests.models import Customer


def test_get_customer_id(cursor: pg.Cursor):

    customer = pg.get_one(
        cursor=cursor[Customer],
        select=(e.id, e.name),
        from_=e.customer,
        where=e.id == 1,
    )

    assert isinstance(customer, Customer)
    assert customer.id == 1


def test_get_customer_by_name(cursor: pg.Cursor):

    customer = pg.get_one(
        cursor=cursor[Customer],
        select=(e.id, e.name),
        from_=e.customer,
        where=e.name == 'Customer B',
    )

    assert isinstance(customer, Customer)
    assert customer.name == 'Customer B'


def test_get_customer_by_invalid_id(cursor: pg.Cursor):

    customer = pg.get_one(
        cursor=cursor[Customer],
        select=(e.id, e.name),
        from_=e.customer,
        where=e.id == 3,
    )

    assert customer is None


def test_get_customer_id_by_name(cursor: pg.Cursor):

    customer_id = pg.get_one(
        cursor=cursor[int],
        select=e.id,
        from_=e.customer,
        where=e.name == 'Customer A',
    )

    assert isinstance(customer_id, int)
    assert customer_id == 1


def test_get_customer_tuple_by_id(cursor: pg.Cursor):

    customer_tuple = pg.get_one(
        cursor=cursor[tuple[int, str]],
        select=(e.id, e.name),
        from_=e.customer,
        where=e.id == 1,
    )

    assert isinstance(customer_tuple, tuple)
    assert customer_tuple[0] == 1
    assert customer_tuple[1] == 'Customer A'
