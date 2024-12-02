from pgcrud import e
from pgcrud.expr import ReferenceExpr


def test_generate_expr():
    user = e.user
    assert type(user) is ReferenceExpr
    assert user.get_composed().as_string() == '"user"'


def test_generate_child_expr():
    user = e.user
    user_name = user.name
    assert type(user_name) is ReferenceExpr
    assert user_name._parent is user
    assert user_name.get_composed().as_string() == '"user"."name"'
