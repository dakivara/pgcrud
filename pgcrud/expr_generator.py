from psycopg.sql import Placeholder

from pgcrud.expr import ReferenceExpr, PlaceholderExpr

__all__ = ['ExprGenerator']


class ExprGeneratorType(type):

    def __getattr__(cls, name) -> ReferenceExpr:
        return ReferenceExpr(name)

    def __call__(cls, name: str) -> ReferenceExpr:
        return ReferenceExpr(name)


class ExprGenerator(metaclass=ExprGeneratorType):

    @staticmethod
    def P(name: str | None = None) -> PlaceholderExpr:
        return PlaceholderExpr(Placeholder(name or ''))
