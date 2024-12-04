import pgcrud as pg
from pgcrud import e

from tests.models import Customer


def test_get_customer_id(cursor):

    customer = pg.get_one(
        cursor=cursor,
        select=Customer,
        from_=e.customer,
        where=e.id == 1,
    )

    assert isinstance(customer, Customer)
    assert customer.id == 1


def test_get_customer_by_name(cursor):

    customer = pg.get_one(
        cursor=cursor,
        select=Customer,
        from_=e.customer,
        where=e.name == 'Customer B',
    )

    assert isinstance(customer, Customer)
    assert customer.name == 'Customer B'


def test_get_customer_by_invalid_id(cursor):

    customer = pg.get_one(
        cursor=cursor,
        select=Customer,
        from_=e.customer,
        where=e.id == 3,
    )

    assert customer is None
