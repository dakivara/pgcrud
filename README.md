# pgcrud

pgcrud is a Python package that makes **C**reate, **R**ead, **U**pdate, and **D**elete (**CRUD**) operations for PostgreSQL simple and fast. 

## Key Features

- No ORM, only declarative expressions.
- Built-in pydantic and msgspec support for data serialization & validation
- Efficient handling of complex parent-child relationships 
- Perform operations sync or async.
- Full type hint support.
- Easy to integrate into existing projects.
- Protection against SQL-Injection
- Tailored to PostgreSQL with wide extensions support.


## Installation

The **pgcrud** package is not yet available on PyPI. However, you can install it using pip with the following command:

```
pip install git+https://github.com/dakivara/pgcrud.git
```

To use pydantic or msgspec, ensure you install them separately, as they are optional dependencies.

Do not download the pgcrud package from PyPi. This is an abandoned package and is not affiliated with us.

## Documentation

The link to the comprehensive documentation is [here](https://pgcrud.com/). Please note that it is still work in progress.

## Example

Imagine you have an Author and Book table in your schema. Each author (the parent) has authored several books (the children). 
With pgcrud you can easily fetch the author including the author's books in a single request and return the result as a Pydantic model.

```python
from pydantic import BaseModel

import pgcrud as pg
from pgcrud import Identifier as i, QueryBuilder as q, functions as f


class Book(BaseModel):
    id: int
    title: str


class Author(BaseModel):
    id: int                  
    name: str             
    books: list[Book]

    
def get_author(cursor: pg.Cursor, id_: int) -> Author | None:
    return pg.get_one(
        cursor=cursor[Author],
        select=(i.author.id, i.author.name, i.author_books.books),
        from_=i.author.
        JOIN(
            q.SELECT(i.author_id, f.json_agg(i.book).AS(i.books)).
            FROM(i.book).
            GROUP_BY(i.author_id).
            AS(i.author_books)
        ).ON(i.author.id == i.author_books.author_id),
        where=i.author.id == id_,
    )


with pg.connect('CONN_STR') as conn:
    with conn.cursor() as cursor:
        author = get_author(cursor, 1)
```

## Main Components

### Identifier

You can import the Identifier with `from pgcrud import Identifier`. The Identifier enables you to define generic references to database objects 
such as columns, tables, views, or subqueries. These references support arithmetic and comparison operations, allow you to define aliases and join 
expressions, and provide additional capabilities for handling complex database operations.

```python
from pgcrud import Identifier as i

(i.age > 18) & (i.age < 60) & (i.id.IN([1, 2, 3]))
# "age" > 18 AND "age" < 60 AND "id" IN (1, 2, 3)

(i.weight / i.height ** 2).AS(i.bmi)
# weight" / ("height" ^ 2) AS "bmi"

i.user.name
# "user"."name"

i.author.AS(i.a).LEFT_JOIN(i.publisher.AS(i.p)).ON(i.a.publisher_id == i.p.id)
# "author" AS "a" LEFT JOIN "publisher" AS "p" ON "a"."publisher_id" = "p"."id"
```


### Query Builder

You can import the Query Builder with `from pgcrud import QueryBuilder`. The Query Builder is used to construct queries and subqueries for performing any CRUD operation.

```python
from pgcrud import Identifier as i, QueryBuilder as q

q.SELECT(i.id, i.name, i.salary).\
FROM(i.employee).\
WHERE(i.salary > 10000)
# SELECT "id", "name", "salary" FROM "employee" WHERE "salary" > 10000

q.INSERT_INTO(i.employee[i.name, i.salary, i.department_id]).\
VALUES(('John Doe', 1000, 1), {'name': 'Jane Doe', 'salary': 2000, 'department_id': 2}).\
RETURNING(i.id)
# INSERT INTO "employee" ("name", "salary", "department_id") VALUES ('John Doe', 1000, 1), ('Jane Doe', 2000, 2) RETURNING "id"

q.UPDATE(i.employee).\
SET((i.salary, i.department_id), (3000, 3)).\
WHERE(i.id == 1)
# UPDATE "employee" SET ("salary", "department_id") = (3000, 3) WHERE "id" = 1

q.DELETE_FROM(i.employee).\
WHERE(i.salary > 10000).\
RETURNING(i.id)
# DELETE FROM "employee" WHERE "salary" > 10000 RETURNING "id"
```


### Functions

You can import the Functions with `from pgcrud import functions`. Each function corresponds to 
a PostgreSQL function. You can use them to declare transformations, aggregations, and more.

```python
from pgcrud import functions as f, Identifier as i

f.avg(i.salary + i.bonus).AS(i.average_compensation)
# avg("salary" + "bonus") AS "average_compensation"

f.to_json(i.publisher).AS(i.publisher)
# to_json("publisher") AS "publisher"
```


## Why choose pgcrud?

When building a Python application with PostgreSQL database, most developers either opt for ORMs (like SQLAlchemy or SQLModel) or write 
raw SQL. Both approaches have their upsides and downsides:

- ORMs: While convenient, ORMs map directly to tables, but real-world applications often require modeling relationships. This leads to additional data models and more database requests, increasing complexity and overhead.
- Raw SQL: Writing raw SQL avoids the abstraction but comes with its own challenges, such as repetitive code and difficulty handling optional filters or sorting conditions effectively.

Unlike traditional ORMs, **pgcrud** enables you to define generic, declarative expressions. This drastically 
reduces the code base and enables highly efficient querying. pgcrud has built-in data serialization and validation and is specifically tailored for 
PostgreSQL, providing a more efficient approach than SQLAlchemy.


## Type Hints
**pgcrud** offers full support for type hints, making it easier to write and maintain your code with better autocompletion and error checking.

- **Recommended Tool**: We recommend using Pyright as it provides accurate and efficient type inference.
- **For PyCharm Users**: We suggest installing the [Pyright plugin](https://github.com/InSyncWithFoo/pyright-for-pycharm) as the standard PyCharm type checker is generally not great. This plugin ensures that type hints are correctly interpreted and validated.
