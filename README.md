# pgcrud

**pgcrud** makes Create, Read, Update, and Delete (CRUD) operations for PostgreSQL simple and fast. It serves as 
the bridge between the popular PostgreSQL adapter psycopg and Pydantic, the leading library for data serialization and validation. 
**pgcrud** redefines ORMs by mapping Python data model annotations to corresponding objects in the database.

## Installation

The **pgcrud** package is not yet available on PyPI. However, you can install it using pip with the following command:

```
pip install git+https://github.com/dakivara/pgcrud.git
```

Do not download the pgcrud package from PyPi. This is an abandoned package and is not affiliated with us.

## Documentation

The link to the comprehensive documentation is [here](https://pgcrud.com/). Please note that it is still work in progress.

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

## Main Components

### Expression Generator

You can import the expression generator with `from pgcrud import e`. The expression generator enables you to define generic references to database objects 
such as columns, tables, views, or subqueries. These references support arithmetic and comparison operations, allow you to define aliases and join 
expressions, and provide additional capabilities for handling complex database operations.

```python
from pgcrud import e

(e.age > 18) & (e.age < 60) & (e.id.IN([1, 2, 3]))
# "age" > 18 AND "age" < 60 AND "id" IN '{1,2,3}::int2[]'

(e.weight / e.height ** 2).AS('bmi')
# weight" / ("height" ^ 2) AS "bmi"

e.user.name
# "user"."name"

e.author.AS('a').LEFT_JOIN(e.publisher.AS('p')).ON(e.a.publisher_id == e.p.id)
# "author" AS "a" LEFT JOIN "publisher" AS "p" ON "a"."publisher_id" = "p"."id"
```


### Function Bearer

You can import the function bearer with `from pgcrud import f`. The function bearer provides access to functions that 
correspond to PostgreSQL functions. You can use it to declare transformations, aggregations, and more.

```python
from pgcrud import e, f

f.avg(e.salary + e.bonus).AS('average_compensation')
# avg("salary" + "bonus") AS "average_compensation"

f.to_json(e.publisher).AS('publisher')
# to_json("publisher") AS "publisher"
```

### Query Builder

You can import the query builder with `from pgcrud import q`. The query builder is used to construct queries and subqueries for performing any CRUD operation.

```python
from pgcrud import e, f, q

q.SELECT((e.department.id, e.department.name, f.avg(e.employee.salary).AS('avg_salary'))).\
FROM(e.employee.JOIN(e.deparment).ON(e.employee.department_id == e.departement.id)).\
GROUP_BY(e.employee.department_id)
# SELECT "department"."id", "department"."name", avg("employee"."salary") AS "avg_salary" FROM "employee" JOIN "deparment" ON "employee"."department_id" = "departement"."id" GROUP BY "employee"."department_id"

q.INSERT_INTO(e.employee[e.name, e.salary, e.department_id]).\
VALUES(('John Doe', 1000, 1), {'name': 'Jane Doe', 'salary': 2000, 'department_id': 2}).\
RETURNING(e.id)
# INSERT INTO "employee" ("name", "salary", "department_id") VALUES ('John Doe', 1000, 1), ('Jane Doe', 2000, 2) RETURNING "id"

q.UPDATE(e.employee).\
SET((e.salary, e.department_id), (3000, 3)).\
WHERE(e.id == 1)
# UPDATE "employee" SET ("salary", "department_id") = (3000, 3) WHERE "id" = 1

q.DELETE_FROM(e.employee).\
WHERE(e.salary > 10000).\
RETURNING(e.id)
# DELETE FROM "employee" WHERE "salary" > 10000 RETURNING "id"
```

## Why choose pgcrud?

When building a Python application with PostgreSQL database, most developers either opt for ORMs (like SQLAlchemy or SQLModel) or write 
raw SQL. Both approaches have their upsides and downsides:

- ORMs: While convenient, ORMs map directly to tables, but real-world applications often require modeling relationships. This leads to additional data models and more database requests, increasing complexity and overhead.
- Raw SQL: Writing raw SQL avoids the abstraction but comes with its own challenges, such as repetitive code and difficulty handling optional filters or sorting conditions effectively.

Unlike traditional ORMs, **pgcrud** uses powerful data annotations to map database objects to Python models only when needed. This drastically 
reduces the code base and enables highly efficient querying. It offers built-in Pydantic integration and is specifically tailored for 
PostgreSQL, providing a more flexible and streamlined approach than SQLAlchemy.

## Type Hints
**pgcrud** offers full support for type hints, making it easier to write and maintain your code with better autocompletion and error checking.

- **Recommended Tool**: We recommend using Pyright as it provides accurate and efficient type inference.
- **For PyCharm Users**: We suggest installing the [Pyright plugin](https://github.com/InSyncWithFoo/pyright-for-pycharm) as the standard PyCharm type checker is generally not great. This plugin ensures that type hints are correctly interpreted and validated.
