
-----

<span style="font-size: 0.9em;">
    **Note**: Make sure to read the [Getting Started](index.md) page first, as it introduces the expression generator and provides an overview of the schema and data used in this tutorial.
</span>

-----

The `get_one` method is designed to retrieve a single record from the database. Based on your requirements, 
it can return a single value, a tuple of values, or a Pydantic model. If no record is found, the method returns `None`.


## Get Pydantic object

Typically, you want to load your fetched record directly into a Pydantic model. You can 
achieve this by passing the Pydantic model to the select parameter of the `get_one` method.

Here is how you can fetch an author by ID.

```python
import psycopg
from pydantic import BaseModel

import pgcrud as pg
from pgcrud import e


class Author(BaseModel):
    id: int
    name: str


with psycopg.connect('YOUR-CONN-STR') as conn:
    with conn.cursor() as cursor:
        author = pg.get_one(
            cursor=cursor, 
            select=Author,
            from_=e.author,
            where=e.id == 1,
        )

print(author)
# id=1 name='J.K. Rowling'
```


## Get nested Pydantic object

Consider the case where you want to fetch an author along with their books. To achieve this, you can define a
nested Pydantic model that represents the relationship between the author and their books. 

You can annotate expressions to Pydantic model fields to refer to corresponding database columns. In the 
code below, the Author model contains a books field, which is a list of Book objects, and the 
relationship is established by joining the author and book tables.

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
        author = pg.get_one(
            cursor=cursor,
            select=Author,   
            from_=e.author.
                JOIN(
                    q.SELECT((e.author_id, f.json_agg(e.book).AS('books'))).
                    FROM(e.book).
                    GROUP_BY(e.author_id).
                    AS('author_books')
                ).ON(e.author.id == e.author_books.author_id),
            where=e.author.id == 1,
        )

print(author)
# id=1 name='J.K. Rowling' books=[Book(id=1, title="Harry Potter and the Sorcerer's Stone"), Book(id=2, title='Harry Potter and the Chamber of Secrets'), Book(id=3, title='Harry Potter and the Prisoner of Azkaban')]
```


## Get single value

If you only need a specific field from a record, you can achieve this by passing a single expression to 
the select parameter of the `get_one` method.

Here is how you fetch the author's name by ID.

```python
import psycopg

import pgcrud as pg
from pgcrud import e


with psycopg.connect('YOUR-CONN-STR') as conn:
    with conn.cursor() as cursor:
        author_name = pg.get_one(
            cursor=cursor, 
            select=e.name,
            from_=e.author,
            where=e.id == 1,
        )

print(author_name)
# J.K. Rowling
```


## Get tuple

If you only need some fields as tuple from a record, you can achieve this by passing a tuple of expressions to 
the select parameter of the `get_one` method.

Here is how you fetch the author's ID and name by ID.

```python
import psycopg

import pgcrud as pg
from pgcrud import e


with psycopg.connect('YOUR-CONN-STR') as conn:
    with conn.cursor() as cursor:
        author_tuple = pg.get_one(
            cursor=cursor, 
            select=(e.id, e.name),
            from_=e.author,
            where=e.id == 1,
        )

print(author_tuple)
# (1, 'J.K. Rowling')
```
