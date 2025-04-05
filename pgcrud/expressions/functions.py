from abc import abstractmethod
from collections.abc import Sequence
from typing import Literal

from pgcrud.expressions.base import Expression, LiteralExpression


__all__ = [
    'FunctionExpression',
    'NowFunctionExpression',
    'RowNumberFunctionExpression',
    'CountFunctionExpression',
    'SumFunctionExpression',
    'AvgFunctionExpression',
    'MinFunctionExpression',
    'MaxFunctionExpression',
    'ArrayAggFunctionExpression',
    'JsonAggFunctionExpression',
    'ToJsonFunctionExpression',
    'JsonBuildObjectFunctionExpression',
    'LowerFunctionExpression',
    'UpperFunctionExpression',
    'CoalesceFunctionExpression',
    'CastFunctionExpression',

    'CryptFunctionExpression',
    'GenSaltFunctionExpression'
]


class FunctionExpression(Expression):

    @abstractmethod
    def __str__(self) -> str:
        pass


class NowFunctionExpression(FunctionExpression):

    def __str__(self) -> str:
        return 'now()'


class RowNumberFunctionExpression(FunctionExpression):

    def __str__(self) -> str:
        return 'row_number()'


class CountFunctionExpression(FunctionExpression):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'count({self.expression})'


class SumFunctionExpression(FunctionExpression):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'sum({self.expression})'


class AvgFunctionExpression(FunctionExpression):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'avg({self.expression})'


class MinFunctionExpression(FunctionExpression):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'min({self.expression})'


class MaxFunctionExpression(FunctionExpression):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'max({self.expression})'


class LowerFunctionExpression(FunctionExpression):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'lower({self.expression})'


class UpperFunctionExpression(FunctionExpression):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'upper({self.expression})'


class ArrayAggFunctionExpression(FunctionExpression):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'array_agg({self.expression})'


class JsonAggFunctionExpression(FunctionExpression):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'json_agg({self.expression})'


class CoalesceFunctionExpression(FunctionExpression):

    def __init__(
            self,
            expressions: Sequence[Expression],
    ):
        self.expressions = expressions

    def __str__(self) -> str:
        return f"coalesce({', '.join([str(expression) for expression in self.expressions])})"


class ToJsonFunctionExpression(FunctionExpression):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'to_json({self.expression})'


class JsonBuildObjectFunctionExpression(FunctionExpression):

    def __init__(
            self,
            expressions: Sequence[Expression],
    ):
        self.expressions = expressions

    def __str__(self) -> str:
        return f"json_build_object({', '.join([str(expression) for expression in self.expressions])})"


class CastFunctionExpression(FunctionExpression):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'cast({self.expression})'


# pgcrypto


class CryptFunctionExpression(FunctionExpression):

    def __init__(
            self,
            password: Expression,
            salt: Expression,
    ):
        self.password = password
        self.salt = salt

    def __str__(self) -> str:
        return f'crypt({self.password}, {self.salt})'


class GenSaltFunctionExpression(FunctionExpression):

    def __init__(
            self,
            algorithm: Literal['bf', 'md5', 'sha256'],
            cost: int | None = None,
    ):
        self.algorithm = LiteralExpression(algorithm)
        self.cost = LiteralExpression(cost) if cost else None

    def __str__(self) -> str:
        if self.cost:
            return f'gen_salt({self.algorithm}, {self.cost})'
        else:
            return f'gen_salt({self.algorithm})'
