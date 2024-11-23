# pgcrud

**pgcrud** is a fast and lightweight library that enables seamless integration between PostgreSQL databases and Pydantic models. 
**pgcrud** simplifies CRUD operations with straightforward functions, eliminating the need for complex classes.

## Installation

**pgcrud** is not yet available on PyPI, but you can install it with pip using the following command:

```
pip install git+https://github.com/dakivara/pgcrud.git
```

## Why choose pgcrud?

**pgcrud** does not attempt to remove writing SQL completely but only replaces SQL with Python code when it's useful. 
It perfectly balances writing SQL and Python code:

- Static SQL elements like table definitions and views are written with SQL.
- Regular CRUD operations are handled with Pgcrud.
- Complex tasks, such as CTEs and advanced queries, are written using SQL.

Since CRUD operations make up a significant part of your codebase, **pgcrud** will help you drastically reduce it.

## Simple Example
