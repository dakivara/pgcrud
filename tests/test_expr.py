from pgcrud.expr import ReferenceExpr


def test_generate_expr():
    user = ReferenceExpr('user')
    assert type(user) is ReferenceExpr
    assert user.get_composed().as_string() == '"user"'


def test_generate_child_expr():
    user = ReferenceExpr('user')
    user_name = user.name
    assert type(user_name) is ReferenceExpr
    assert user_name._parent is user
    assert user_name.get_composed().as_string() == '"user"."name"'


def test_arithmetic_operations():
    a = None
    b = ReferenceExpr('b')
    c = 1

    assert (a + b + c).get_composed().as_string() == 'NULL + "b" + 1'
    assert (a - b - c).get_composed().as_string() == 'NULL - "b" - 1'
    assert (a * b + c).get_composed().as_string() == '(NULL * "b") + 1'
    assert (a * (b + c)).get_composed().as_string() == 'NULL * ("b" + 1)'
    assert (a / b - c).get_composed().as_string() == '(NULL / "b") - 1'
    assert (a / (b - c)).get_composed().as_string() == 'NULL / ("b" - 1)'
    assert (a / b ** c).get_composed().as_string() == 'NULL / ("b" ^ 1)'
    assert ((a / b) ** c).get_composed().as_string() == '(NULL / "b") ^ 1'


def test_comparison_operations():
    a = ReferenceExpr('a')
    b = ReferenceExpr('b')

    assert (a == b).get_composed().as_string() == '"a" = "b"'
    assert (a != b).get_composed().as_string() == '"a" <> "b"'
    assert (a < b).get_composed().as_string() == '"a" < "b"'
    assert (a <= b).get_composed().as_string() == '"a" <= "b"'
    assert (a > b).get_composed().as_string() == '"a" > "b"'
    assert (a >= b).get_composed().as_string() == '"a" >= "b"'
    assert a.IN([1, 2]).get_composed().as_string() == '"a" IN (1, 2)'
    assert a.NOT_IN([1, 2]).get_composed().as_string() == '"a" NOT IN (1, 2)'
    assert a.IS_NULL().get_composed().as_string() == '"a" IS NULL'
    assert a.IS_NOT_NULL().get_composed().as_string() == '"a" IS NOT NULL'


def test_sort_operations():
    a = ReferenceExpr('a')

    assert a.ASC().get_composed().as_string() == '"a" ASC'
    assert a.ASC(True).get_composed().as_string() == '"a" ASC'
    assert a.ASC(False).get_composed().as_string() == '"a" DESC'
    assert a.DESC().get_composed().as_string() == '"a" DESC'
    assert a.DESC(True).get_composed().as_string() == '"a" DESC'
    assert a.DESC(False).get_composed().as_string() == '"a" ASC'
