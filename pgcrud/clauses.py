from __future__ import annotations

from abc import abstractmethod
from typing import Any, Sequence, TYPE_CHECKING

from psycopg.sql import Literal as _Literal

from pgcrud.optional_dependencies import (
    is_pydantic_installed,
    is_pydantic_instance,
    pydantic_to_dict,
    is_msgspec_installed,
    is_msgspec_instance,
    msgspec_to_dict,
)
from pgcrud.types import SequenceType

if TYPE_CHECKING:
    from pgcrud.expressions import Expression, Literal, Undefined, Unbounded, CurrentRow, Identifier, TableIdentifier, DerivedTable
    from pgcrud.filter_conditions import FilterCondition


__all__ = [
    'Clause',
    'As',
    'Asc',
    'CrossJoin',
    'DeleteFrom',
    'Desc',
    'DoNothing',
    'DoUpdate',
    'Filter',
    'Following',
    'From',
    'FullJoin',
    'GroupBy',
    'Having',
    'InnerJoin',
    'InsertInto',
    'Join',
    'LeftJoin',
    'Limit',
    'Offset',
    'On',
    'OnConflict',
    'OnConstraint',
    'OrderBy',
    'Over',
    'PartitionBy',
    'Preceding',
    'RangeBetween',
    'Returning',
    'RightJoin',
    'RowsBetween',
    'Select',
    'Set',
    'Update',
    'Using',
    'Values',
    'Where',
    'Window',
    'With',
]


class Clause:

    _tag = 'CLAUSE'

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return str(self)

    def __bool__(self) -> bool:
        return True


class As(Clause):

    def __init__(
            self,
            alias: Expression,
    ):
        self.alias = alias

    def __str__(self) -> str:
        return f'AS {self.alias}'


class Asc(Clause):

    def __init__(
            self,
            flag: bool | Undefined = True,
    ):
        self.flag = flag

    def __str__(self) -> str:
        if self:
            if self.flag:
                return 'ASC'
            else:
                return 'DESC'
        else:
            return ''

    def __bool__(self) -> bool:
        return isinstance(self.flag, bool)


class CrossJoin(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'CROSS JOIN {self.expression}'


class DeleteFrom(Clause):

    def __init__(
            self,
            identifier: Identifier,
    ):
        self.identifier = identifier

    def __str__(self) -> str:
        return f'DELETE FROM {self.identifier}'


class Desc(Clause):

    def __init__(
            self,
            flag: bool | Undefined = True,
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


class DoNothing(Clause):

    def __str__(self) -> str:
        return 'DO NOTHING'


class DoUpdate(Clause):

    def __str__(self) -> str:
        return 'DO UPDATE'


class Filter(Clause):

    def __init__(
            self,
            where: Where,
    ):
        self.where = where

    def __str__(self) -> str:
        return f'FILTER ({self.where})'


class Following(Clause):

    def __str__(self) -> str:
        return 'FOLLOWING'


class From(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'FROM {self.expression}'


class FullJoin(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'FULL JOIN {self.expression}'


class GroupBy(Clause):

    def __init__(
            self,
            exprs: list[Expression],
    ):
        self.exprs = exprs

    def __str__(self) -> str:
        return f"GROUP BY {', '.join([str(expr) for expr in self.exprs])}"


class Having(Clause):

    def __init__(
            self,
            condition: FilterCondition,
    ):
        self.condition = condition

    def __str__(self) -> str:
        if self:
            return f'HAVING {self.condition}'
        else:
            return ''

    def __bool__(self) -> bool:
        return bool(self.condition)


class InnerJoin(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'INNER JOIN {self.expression}'


class InsertInto(Clause):

    def __init__(
            self,
            identifier: Identifier | TableIdentifier,
    ):
        self.identifier = identifier

    def __str__(self) -> str:
        return f'INSERT INTO {self.identifier}'


class Join(Clause):

    def __init__(
            self,
            expr: Expression,
    ):
        self.expr = expr

    def __str__(self) -> str:
        return f'JOIN {self.expr}'


class LeftJoin(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'LEFT JOIN {self.expression}'


class Limit(Clause):

    def __init__(
            self,
            value: int,
    ):
        self.value = value

    def __str__(self) -> str:
        return f'LIMIT {self.value}'


class Offset(Clause):

    def __init__(
            self,
            value: int,
    ):
        self.value = value

    def __str__(self) -> str:
        return f'OFFSET {self.value}'


class On(Clause):

    def __init__(
            self,
            condition: FilterCondition,
    ):
        self.condition = condition

    def __str__(self) -> str:
        return f'ON {self.condition}'


class OnConflict(Clause):

    def __str__(self) -> str:
        return 'ON CONFLICT'


class OnConstraint(Clause):

    def __init__(
            self,
            identifier: Identifier,
    ):
        self.identifier = identifier

    def __str__(self) -> str:
        return f'ON CONSTRAINT {self.identifier}'


class OrderBy(Clause):

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


class Over(Clause):

    def __init__(
            self,
            derived_table: DerivedTable,
    ):
        self.derived_table = derived_table

    def __str__(self) -> str:
        return f'OVER {self.derived_table}'


class PartitionBy(Clause):

    def __init__(
            self,
            expressions: Sequence[Expression],
    ):
        self.expressions = expressions

    def __str__(self) -> str:
        return f"PARTITION BY {', '.join([str(expression) for expression in self.expressions])}"


class Preceding(Clause):

    def __str__(self) -> str:
        return 'PRECEDING'


class RangeBetween(Clause):

    def __init__(
            self,
            start: Literal | Unbounded | CurrentRow,
            end: Literal | Unbounded | CurrentRow,
    ):
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f'RANGE BETWEEN {self.start} {self.end}'


class Returning(Clause):

    def __init__(
            self,
            expressions: Sequence[Expression],
    ):
        self.expressions = expressions

    def __str__(self) -> str:
        return f"RETURNING {', '.join([str(expression) for expression in self.expressions])}"


class RightJoin(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'RIGHT JOIN {self.expression}'


class RowsBetween(Clause):

    def __init__(
            self,
            start: Literal | Unbounded | CurrentRow,
            end: Literal | Unbounded | CurrentRow,
    ):
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f'ROWS BETWEEN {self.start} {self.end}'


class Select(Clause):

    def __init__(
            self,
            expressions: Sequence[Expression],
    ):
        self.expressions = expressions

    def __str__(self) -> str:
        return f"SELECT {', '.join([str(expression) for expression in self.expressions])}"


class Set(Clause):

    def __init__(
            self,
            columns: Sequence[Identifier],
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
                val_strs.append(_Literal(params[identifier._name]).as_string())

        elif is_msgspec_installed and is_msgspec_instance(self.values):
            params = msgspec_to_dict(self.values)
            params.update(self.additional_values)
            for identifier in self.columns:
                col_strs.append(str(identifier))
                val_strs.append(_Literal(params[identifier._name]).as_string())

        elif isinstance(self.values, dict):
            params = self.values
            params.update(self.additional_values)
            for identifier in self.columns:
                col_strs.append(str(identifier))
                val_strs.append(_Literal(params[identifier._name]).as_string())

        elif isinstance(self.values, SequenceType):
            for identifier, val in zip(self.columns, self.values, strict=True):
                col_strs.append(str(identifier))
                val_strs.append(_Literal(val).as_string())

        else:
            for identifier, val in zip(self.columns, [self.values], strict=True):
                col_strs.append(str(identifier))
                val_strs.append(_Literal(val).as_string())

        if len(col_strs) < 2:
            return f"SET {col_strs[0]} = {val_strs[0]}"
        else:
            return f"SET ({', '.join(col_strs)}) = ({', '.join(val_strs)})"


class Update(Clause):

    def __init__(
            self,
            identifier: Identifier,
    ):
        self.identifier = identifier

    def __str__(self) -> str:
        return f'UPDATE {self.identifier}'


class Using(Clause):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'USING {self.expression}'


class Values(Clause):

    def __init__(
            self,
            values: Sequence[Any],
            additional_values: dict[str, Any],
            order: Sequence[Identifier] | None = None,
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
                    str_item = ', '.join([_Literal(params[identifier._name]).as_string() for identifier in self.order])
                else:
                    str_item = ', '.join(_Literal(v).as_string() for v in params.values())
                str_list.append(f'({str_item})')

            elif is_msgspec_installed and is_msgspec_instance(value):
                params = msgspec_to_dict(value)
                params.update(self.additional_values)
                if self.order:
                    str_item = ', '.join([_Literal(params[identifier._name]).as_string() for identifier in self.order])
                else:
                    str_item = ', '.join(_Literal(v).as_string() for v in params.values())
                str_list.append(f'({str_item})')

            elif isinstance(value, dict):
                params = value.copy()
                params.update(self.additional_values)
                if self.order:
                    str_item = ', '.join([_Literal(params[identifier._name]).as_string() for identifier in self.order])
                else:
                    str_item = ', '.join(_Literal(v).as_string() for v in params.values())
                str_list.append(f'({str_item})')

            elif isinstance(value, SequenceType):
                str_list.append(f"({', '.join(_Literal(v).as_string() for v in value)})")

            else:
                str_list.append(f"({_Literal(value).as_string()})")

        return f"VALUES {', '.join(str_list)}"


class Where(Clause):

    def __init__(
            self,
            condition: FilterCondition,
    ):
        self.condition = condition

    def __str__(self) -> str:
        if self:
            return f'WHERE {self.condition}'
        else:
            return ''

    def __bool__(self) -> bool:
        return bool(self.condition)


class Window(Clause):

    def __init__(
            self,
            identifiers: Sequence[Identifier],
    ):
        self.identifiers = identifiers

    def __str__(self) -> str:
        return f"WINDOW {','.join([str(identifier) for identifier in self.identifiers])}"


class With(Clause):

    def __init__(
            self,
            identifiers: Sequence[Identifier],
    ):
        self.identifiers = identifiers

    def __str__(self) -> str:
        return f"WITH {','.join([str(identifier) for identifier in self.identifiers])}"
