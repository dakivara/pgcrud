from __future__ import annotations

from abc import abstractmethod
from typing import Any, Sequence

from pgcrud.expressions.base import (
    make_expr,
    Expression,
    IdentifierExpression,
    UndefinedExpression,
)
from pgcrud.optional_dependencies import (
    is_pydantic_installed,
    is_pydantic_instance,
    pydantic_to_dict,
    is_msgspec_installed,
    is_msgspec_instance,
    msgspec_to_dict,
)
from pgcrud.types import SequenceType


__all__ = [
    'Clause',
    'AsClause',
    'DeleteFromClause',
    'DescClause',
    'DoNothingClause',
    'DoUpdateClause',
    'FollowingClause',
    'FromClause',
    'GroupByClause',
    'HavingClause',
    'InClause',
    'InsertIntoClause',
    'LimitClause',
    'OffsetClause',
    'OnClause',
    'OnConflictExpression',
    'OnConstraintClause',
    'OrderByClause',
    'OverClause',
    'PartitionByClause',
    'PrecedingClause',
    'RangeBetweenClause',
    'ReturningClause',
    'RowsBetweenClause',
    'SelectClause',
    'SetClause',
    'UpdateClause',
    'UsingClause',
    'ValuesClause',
    'WhereClause',
    'WindowClause',
    'WithClause',
]


class Clause:

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return str(self)

    def __bool__(self) -> bool:
        return True


class AsClause(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'AS {self.expression}'


class DeleteFromClause(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'DELETE FROM {self.expression}'


class DescClause(Clause):

    def __init__(
            self,
            flag: bool | UndefinedExpression = True,
    ):
        self.flag = flag

    def __str__(self) -> str:
        if self:
            if self.flag:
                return 'DESC'
            else:
                return 'ASC'
        else:
            return ''


class DoNothingClause(Clause):

    def __str__(self) -> str:
        return 'DO NOTHING'


class DoUpdateClause(Clause):

    def __str__(self) -> str:
        return 'DO UPDATE'


class FollowingClause(Clause):

    def __str__(self) -> str:
        return 'FOLLOWING'


class FromClause(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'FROM {self.expression}'


class GroupByClause(Clause):

    def __init__(
            self,
            expressions: list[Expression],
    ):
        self.expressions = expressions

    def __str__(self) -> str:
        return f"GROUP BY {', '.join([str(expression) for expression in self.expressions])}"


class HavingClause(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        if self:
            return f'HAVING {self.expression}'
        else:
            return ''

    def __bool__(self) -> bool:
        return bool(self.expression)


class InClause(Clause):

    def __init__(
            self,
            expressions: list[Expression],
    ):
        self.expressions = expressions

    def __str__(self):
        if self:
            return f"IN ({', '.join([str(expression) for expression in self.expressions if expression])})"
        else:
            return ''

    def __bool__(self) -> bool:
        return any(self.expressions)


class InsertIntoClause(Clause):

    def __init__(
            self,
            identifier_expression: IdentifierExpression,
    ):
        self.identifier_expression = identifier_expression

    def __str__(self) -> str:
        return f'INSERT INTO {self.identifier_expression}'


class LimitClause(Clause):

    def __init__(
            self,
            value: int,
    ):
        self.value = value

    def __str__(self) -> str:
        return f'LIMIT {self.value}'


class OffsetClause(Clause):

    def __init__(
            self,
            value: int,
    ):
        self.value = value

    def __str__(self) -> str:
        return f'OFFSET {self.value}'


class OnClause(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'ON {self.expression}'


class OnConflictExpression(Clause):

    def __str__(self) -> str:
        return 'ON CONFLICT'


class OnConstraintClause(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'ON CONSTRAINT {self.expression}'


class OrderByClause(Clause):

    def __init__(
            self,
            expressions: Sequence[Expression],
    ):
        self.expressions = expressions

    def __str__(self) -> str:
        if self:
            return f"ORDER BY {', '.join(str(expression) for expression in self.expressions if expression)}"
        else:
            return ''

    def __bool__(self) -> bool:
        return any(self.expressions)


class OverClause(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'OVER {self.expression}'


class PartitionByClause(Clause):

    def __init__(
            self,
            expressions: Sequence[Expression],
    ):
        self.expressions = expressions

    def __str__(self) -> str:
        return f"PARTITION BY {', '.join([str(expression) for expression in self.expressions])}"


class PrecedingClause(Clause):

    def __str__(self) -> str:
        return 'PRECEDING'


class RangeBetweenClause(Clause):

    def __init__(
            self,
            start: Expression,
            end: Expression,
    ):
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f'RANGE BETWEEN {self.start} {self.end}'


class ReturningClause(Clause):

    def __init__(
            self,
            expressions: Sequence[Expression],
    ):
        self.expressions = expressions

    def __str__(self) -> str:
        return f"RETURNING {', '.join([str(expression) for expression in self.expressions])}"


class RowsBetweenClause(Clause):

    def __init__(
            self,
            start: Expression,
            end: Expression,
    ):
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f'ROWS BETWEEN {self.start} {self.end}'


class SelectClause(Clause):

    def __init__(
            self,
            expressions: Sequence[Expression],
    ):
        self.expressions = expressions

    def __str__(self) -> str:
        return f"SELECT {', '.join([str(expression) for expression in self.expressions])}"


class SetClause(Clause):

    def __init__(
            self,
            columns: Sequence[IdentifierExpression],
            values: Any,
            additional_values: dict[str, Any],
    ):
        self.columns = columns
        self.values = values
        self.additional_values = additional_values

    def __str__(self) -> str:

        col_strs = []
        val_strs = []

        if is_pydantic_installed and is_pydantic_instance(self.values):
            params = pydantic_to_dict(self.values)
            params.update(self.additional_values)
            for identifier in self.columns:
                col_strs.append(str(identifier))
                val_strs.append(str(make_expr(params[identifier._name])))

        elif is_msgspec_installed and is_msgspec_instance(self.values):
            params = msgspec_to_dict(self.values)
            params.update(self.additional_values)
            for identifier in self.columns:
                col_strs.append(str(identifier))
                val_strs.append(str(make_expr(params[identifier._name])))

        elif isinstance(self.values, dict):
            params = self.values
            params.update(self.additional_values)
            for identifier in self.columns:
                col_strs.append(str(identifier))
                val_strs.append(str(make_expr(params[identifier._name])))

        elif isinstance(self.values, SequenceType):
            for identifier, val in zip(self.columns, self.values, strict=True):
                col_strs.append(str(identifier))
                val_strs.append(str(make_expr(val)))

        else:
            for identifier, val in zip(self.columns, [self.values], strict=True):
                col_strs.append(str(identifier))
                val_strs.append(str(make_expr(val)))

        if len(col_strs) < 2:
            return f"SET {col_strs[0]} = {val_strs[0]}"
        else:
            return f"SET ({', '.join(col_strs)}) = ({', '.join(val_strs)})"


class UpdateClause(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'UPDATE {self.expression}'


class UsingClause(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'USING {self.expression}'


class ValuesClause(Clause):

    def __init__(
            self,
            values: Sequence[Any],
            additional_values: dict[str, Any],
            order: Sequence[IdentifierExpression] | None = None,
    ):
        self.values = values
        self.additional_values = additional_values
        self.order = order

    def __str__(self) -> str:

        str_list = []

        for value in self.values:

            if is_pydantic_installed and is_pydantic_instance(value):
                params = pydantic_to_dict(value)
                params.update(self.additional_values)
                if self.order:
                    str_item = ', '.join([str(make_expr(params[identifier._name])) for identifier in self.order])
                else:
                    str_item = ', '.join(str(make_expr(v)) for v in params.values())
                str_list.append(f'({str_item})')

            elif is_msgspec_installed and is_msgspec_instance(value):
                params = msgspec_to_dict(value)
                params.update(self.additional_values)
                if self.order:
                    str_item = ', '.join([str(make_expr(params[identifier._name])) for identifier in self.order])
                else:
                    str_item = ', '.join(str(make_expr(v)) for v in params.values())
                str_list.append(f'({str_item})')

            elif isinstance(value, dict):
                params = value.copy()
                params.update(self.additional_values)
                if self.order:
                    str_item = ', '.join([str(make_expr(params[identifier._name])) for identifier in self.order])
                else:
                    str_item = ', '.join(str(make_expr(v)) for v in params.values())
                str_list.append(f'({str_item})')

            elif isinstance(value, SequenceType):
                str_list.append(f"({', '.join(str(make_expr(v)) for v in value)})")

            else:
                str_list.append(f"({make_expr(value)})")

        return f"VALUES {', '.join(str_list)}"


class WhereClause(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        if self:
            return f'WHERE {self.expression}'
        else:
            return ''

    def __bool__(self) -> bool:
        return bool(self.expression)


class WindowClause(Clause):

    def __init__(
            self,
            expressions: Sequence[Expression],
    ):
        self.expressions = expressions

    def __str__(self) -> str:
        return f"WINDOW {','.join([str(expression) for expression in self.expressions])}"


class WithClause(Clause):

    def __init__(
            self,
            expressions: Sequence[Expression],
    ):
        self.expressions = expressions

    def __str__(self) -> str:
        return f"WITH {','.join([str(expression) for expression in self.expressions])}"
