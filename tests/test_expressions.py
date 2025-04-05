from pgcrud import IdentifierExpression


def test_generate_expr():
    user = IdentifierExpression('user')
    assert type(user) is IdentifierExpression
    assert str(user) == '"user"'


def test_generate_child_expr():
    user = IdentifierExpression('user')
    user_name = user.name
    assert type(user_name) is IdentifierExpression
    assert user_name._parent is user
    assert str(user_name) == '"user"."name"'


def test_arithmetic_operations():
    a = None
    b = IdentifierExpression('b')
    c = 1

    assert str(a + b + c) == 'NULL + "b" + 1'
    assert str(a - b - c) == 'NULL - "b" - 1'
    assert str(a * b + c) == '(NULL * "b") + 1'
    assert str(a * (b + c)) == 'NULL * ("b" + 1)'
    assert str(a / b - c) == '(NULL / "b") - 1'
    assert str(a / (b - c)) == 'NULL / ("b" - 1)'
    assert str(a / b ** c) == 'NULL / ("b" ^ 1)'
    assert str((a / b) ** c) == '(NULL / "b") ^ 1'


def test_comparison_operations():
    a = IdentifierExpression('a')
    b = IdentifierExpression('b')

    assert str(a == b) == '"a" = "b"'
    assert str(a != b) == '"a" <> "b"'
    assert str(a < b) == '"a" < "b"'
    assert str(a <= b) == '"a" <= "b"'
    assert str(a > b) == '"a" > "b"'
    assert str(a >= b) == '"a" >= "b"'
    assert str(a.IN([1, 2])) == '"a" IN (1, 2)'
    assert str(a.NOT_IN([1, 2])) == '"a" NOT IN (1, 2)'
    assert str(a.IS(None)) == '"a" IS NULL'
    assert str(a.IS_NOT(None)) == '"a" IS NOT NULL'
