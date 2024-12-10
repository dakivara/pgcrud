
-----

<span style="font-size: 0.9em;">
    **Note**: Make sure to read the [Getting Started](index.md) and [Demo Schema](demo-schema.md) first, as it is essential for better understanding of this tutorial.
</span>

-----

pgcrud provides two functions to perform read operations:

- `get_one`: Returns a single record. If no record is found, the method returns `None`. If more than one records are found, the method returns the first one.
- `get_many`: Returns either a list of records or an iterable cursor.

The following parameters are available:

- `cursor`: Cursor from `psycopg` for execution
- `select`: To specify the selected columns.
- `from_`: To define the target source.[^1]
- `where`: To filter records.
- `group_by`: To group by columns.
- `having`: To filter by aggregated columns.
- `window`: To define windows.
- `order_by`: To sort by columns.
- `limit`: To limit the number of records.[^2]
- `offset`: To skip the first n records.
- `no_fetch`: To execute only.[^2]


[^1]: The only reason why this parameter has a trailing underscore is that `from` is a reserved keyword.

[^2]: Only available for the `get_many` method. 


We go through each of the parameters and show you how to use them.


## Cursor

The `cursor` parameter is explained in detail [here](cursor.md).


## Select

The `select` parameter is required and expects either

- an expression to return a scalar.
- a sequence of expressions to return a tuple.
- a Pydantic model to return an instance of the model.


### Scalar

Pass a single expression to the `select` parameter when you want to retrieve only one column.

```python
from psycopg import Cursor

import pgcrud as pg
from pgcrud import e


def get_author_name(
        cursor: Cursor[str], 
        id_: int,
) -> str | None:
    
    return pg.get_one(
        cursor=cursor,
        select=e.name,
        from_=e.author,
        where=e.id == id_,
    )
    

def get_book_titles(
        cursor: Cursor[str], 
        author_id: int,
) -> list[str]:
    
    return pg.get_many(
        cursor=cursor,
        select=e.title,
        from_=e.book,
        where=e.author_id == author_id,
    )
```


### Tuple

Pass a sequence of expressions to the `select` parameter when you want to retrieve multiple columns as a tuple.


```python
from datetime import date

from psycopg import Cursor

import pgcrud as pg
from pgcrud import e


def get_author_name_and_day_of_birth(
        cursor: Cursor[tuple[str, date]], 
        id_: int,
) -> tuple[str, date] | None:
    
    return pg.get_one(
        cursor=cursor,
        select=(e.name, e.day_of_birth),
        from_=e.author,
        where=e.id == id_,
    )


def get_book_ids_and_titles(
        cursor: Cursor[tuple[int, str]],
        author_id: int,
) -> list[tuple[int, str]]:
    
    return pg.get_many(
        cursor=cursor,
        select=(e.id, e.title),
        from_=e.book,
        where=e.author_id == author_id,
    )
```


### Pydantic Instance

Pass a Pydantic model to the `select` parameter when you want to directly load the retrieved records into the Pydantic model. By default, pgcrud 
maps the Pydantic model field names to the corresponding columns in the target table. However, you can customize this mapping by 
adding expression annotations to each field.

```python
from datetime import date
from typing import Annotated

from psycopg import Cursor
from pydantic import BaseModel

import pgcrud as pg
from pgcrud import e


class Author(BaseModel):
    id: int
    name: str
    dob: Annotated[date, e.date_of_birth]

    
class Book(BaseModel):
    id: int
    title: str


def get_author(
        cursor: Cursor[Author], 
        id_: int,
) -> Author | None:
    
    return pg.get_one(
        cursor=cursor,
        select=Author,
        from_=e.author,
        where=e.id == id_,
    )


def get_books(
        cursor: Cursor[Book],
        author_id: int,
) -> list[Book]:
    
    return pg.get_many(
        cursor=cursor,
        select=Book,
        from_=e.book,
        where=e.author_id == author_id,
    )
```

## From

The `from_` parameter is required and specifies the target source. The target is typically a table or view but it can also 
be a joined table, or a subquery.


### Table (or View)

Pass an expression to the `from_` parameter to directly select from a table or view. 





### Joined Table


### Subquery



## Where


## Group By


## Having


## Window


## Order By


## Limit


## Offset


## No Fetch

