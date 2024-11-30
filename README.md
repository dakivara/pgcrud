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

The **pgcrud** documentation is currently under development. We are working on providing comprehensive guides, examples, and 
API references. Please be a little more patient.

## Example

Here we demonstrate how to manage relationships (parent and children) using **pgcrud**. Imagine you have an Author 
model that belongs to a Publisher (the parent) and has authored several Books (the children). With **pgcrud**, you can 
efficiently fetch a list of authors as Pydantic models, including their associated publisher and books, all in a single request.

```python
from typing import Annotated

import psycopg
from pydantic import BaseModel

import pgcrud as pg
from pgcrud import e, q, f


class Publisher(BaseModel):
    id: int
    name: str
    address: str


class Book(BaseModel):
    id: int
    title: str
    pages: int


# Define the select statement using annotations
class Author(BaseModel):
    id: Annotated[int, e.author.id]                                          # Selects the 'id' column from the 'author' table
    name: Annotated[str, e.author.name]                                      # Selects the 'name' column from the 'author' table
    email: str                                                               # No annotation needed; the field is uniquely identified by its name (annotation still recommended)
    publisher: Annotated[Publisher, f.to_json(e.publisher).AS('publisher')]  # Defines the 'to_json' transformation on the joined 'publisher' table 
    books: Annotated[list[Book], e.author_books.books]                       # Selects 'books' from a 'author_books' subquery


conn_str = 'YOUR-CONNECTION-STRING'

with psycopg.connect(conn_str) as conn:
    with conn.cursor() as cursor:
        authors = pg.get_many(
            cursor=cursor,
            select=Author,   # Maps the result to the Author Pydantic model
            from_=e.author,  # Specifies the main table to query from
            join=(
                # Joins the publisher table on the author's publisher_id
                e.publisher.on(e.author.publisher_id == e.publisher.id, how='INNER'),

                # Joins a subquery to fetch books grouped by author_id
                q.SELECT((e.author_id, f.json_agg(e.book).AS('books'))).   # Selects author_id and JSON aggregated books
                FROM(e.book).                                              # Specifies the book table for the subquery
                GROUP_BY(e.author_id).                                     # Groups books by author_id
                AS('author_books').                                        # Defines the 'author_books' alias
                ON(e.author.id == e.author_books.author_id, how='INNER'),  # Joins subquery on author_id
            ),
            where=e.publisher.id == 1,  # Filters authors by publisher_id = 1
            order_by=e.author.id,       # Orders results by author ID
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

e.publisher.AS('p').on(e.author.id == e.p.author_id)
# "publisher" AS "p" ON "author"."id" = "p"."author_id"
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
FROM(e.employee).\
JOIN(e.deparment.on(e.employee.department_id == e.departement.id)).\
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
