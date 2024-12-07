# Welcome to pgcrud

pgcrud is a Python package that makes **Create**, **Read**, **Update**, and **Delete** (**CRUD**) operations for PostgreSQL simple and fast. 

- **Pydantic**: Native Pydantic model integration.
- **PostgreSQL**: Tailored to PostgreSQL with wide extensions support.
- **Relations**: Handle complex parent-child relationships.
- **Lightweight**: Easy integration into existing projects.
- **Type Hints**: Full type hint support, making it easier to write and maintain your code.
- **Declarative**: Generic data annotations to map database objects to Python models.

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

Imagine you have an Author and Book table in your schema. Each author (the parent) has authored several books (the children). 
With pgcrud you can easily fetch the authors including their books in a single request and return the result as a list of Pydantic models.

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

## License

pgcrud is released under the MIT License.
