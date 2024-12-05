# Welcome to pgCRUD

pgcrud is a Python package that makes **Create**, **Read**, **Update**, and **Delete** (**CRUD**) operations for PostgreSQL simple and fast. 

- **Lightweight**: You can easily integrate pgcrud in your existing projects.
- **Relations**: With pgcrud you can handle complex parent-child relationships.
- **Declarative**: pgcrud uses generic data annotations to map database objects to Python models.
- **Pydantic**: Directly load query result sets into Pydantic models.
- **PostgreSQL**: pgcrud is dedicated solely to PostgreSQL and offers support for a wide range of extensions.

## Dependencies

pgcrud is build on top of

- [psycopg](https://www.psycopg.org): the popular PostgreSQL adapter
- [pydantic](https://docs.pydantic.dev/latest/): the #1 library for data serialization and validation.

## Installation

pgcrud is not yet available on PyPI. However, you can install it using pip with the following command:

```
pip install git+https://github.com/dakivara/pgcrud.git
```

Do not download the pgcrud package from PyPi. This is an abandoned package and is not affiliated with us.


## Example

Imagine you have an Author and Book table in your database schema. Each author (the parent) has authored several books (the children). 
With pgcrud, you can efficiently fetch a list of authors as Pydantic models in a single request.

```python
from typing import Annotated

import psycopg
from pydantic import BaseModel

import pgcrud as pg
from pgcrud import e, q, f


class Book(BaseModel):
    id: int
    title: str


class Author(BaseModel):
    id: Annotated[int, e.author.id]                     
    name: Annotated[str, e.author.name]                 
    books: Annotated[list[Book], e.author_books.books]


with psycopg.connect('YOUR-CONN-STR') as conn:
    with conn.cursor() as cursor:
        authors = pg.get_many(
            cursor=cursor,
            select=Author,   
            from_=e.author.
                JOIN(
                    q.SELECT((e.author_id, f.json_agg(e.book).AS('books'))).
                    FROM(e.book).
                    GROUP_BY(e.author_id).
                    AS('author_books')
                ).ON(e.author.id == e.author_books.author_id),
        )
```
