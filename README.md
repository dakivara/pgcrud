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
from pgcrud import t, c, q, f


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
    id: Annotated[int, t.author.c.id]                                           # Selects the 'id' column from the 'author' table
    name: Annotated[str, t.author.c.name]                                       # Selects the 'name' column from the 'author' table
    email: str                                                                  # No annotation needed; the field is uniquely identified by its name (annotation still recommended)
    publisher: Annotated[Publisher, f.to_json(t.publisher).as_('publisher')]    # Defines the 'to_json' transformation on the joined 'publisher' table 
    books: Annotated[list[Book], t.author_books.c.books]                        # Selects 'books' from a 'author_books' subquery


conn_str = 'YOUR-CONNECTION-STRING'

with psycopg.connect(conn_str) as conn:
    with conn.cursor() as cursor:
        authors = pg.get_many(
            cursor=cursor,
            select=Author,                                                                  # Maps the result to the Author Pydantic model
            from_=t.author,                                                                 # Specifies the main table to query from
            join=(
                # Joins the publisher table on the author's publisher_id
                t.publisher.on(t.author.c.publisher_id == t.publisher.c.id, how='INNER'),
                
                # Joins a subquery to fetch books grouped by author_id
                q.select((c.author_id, f.json_agg(t.book).as_('books'))).                   # Selects author_id and JSON aggregated books
                    from_(t.book).                                                          # Specifies the book table for the subquery
                    group_by(c.author_id).                                                  # Groups books by author_id
                    as_('author_books').                                                    # Defines the 'author_books' alias
                    on(t.author.c.id == t.author_books.c.author_id, how='INNER'),           # Joins subquery on author_id
            ),
            where=t.publisher.c.id == 1,                                                    # Filters authors by publisher_id = 1
            order_by=t.author.c.id,                                                         # Orders results by author ID
        )
```

## Main Components

### Column Generator

You can import the column generator with `from pgcrud import c`. The column generator allows you to define generic references to columns 
in a table, view, or subquery. These references fully support arithmetic and comparison operations, allow you to define aliases, and offer much more flexibility.

```python
from pgcrud import c

(c.age > 18) & (c.age < 60) & (c.id.is_in([1, 2, 3])) 
# "age" > 18 AND "age" < 60 AND "id" IN '{1,2,3}::int2[]'

(c.weight / c.height ** 2).as_('bmi')
# weight" / ("height" ^ 2) AS "bmi"
```


### Table Generator

You can import the table generator with `from pgcrud import t`. The table generator allows you to define generic 
references to a table (or view). Each table reference has access to the column generator for defining table/column 
references, and offers the ability to define aliases, create join expressions, and much more.

```python
from pgcrud import t

t.user.c.name
# "user"."name"

t.publisher.as_('p').on(t.author.c.id == t.p.c.author_id)
# "publisher" AS "p" ON "author"."id" = "p"."author_id"
```

### Function Bearer

You can import the function bearer with `from pgcrud import f`. The function bearer provides access to functions that 
correspond to PostgreSQL functions. You can use it to declare transformations, aggregations, and more.

```python
from pgcrud import c, f, t

f.avg(c.salary + c.bonus).as_('average_compensation')
# avg("salary" + "bonus") AS "average_compensation"

f.to_json(t.publisher).as_('publisher')
# to_json("publisher") AS "publisher"
```

### Query Builder

You can import the query builder with `from pgcrud import q`. The query builder is used to construct queries and subqueries for performing any CRUD operation.

```python
from pgcrud import c, f, q, t


q.select((t.department.c.id, t.department.c.name, f.avg(t.employee.c.salary).as_('avg_salary'))).\
    from_(t.employee).\
    join(t.deparment.on(t.employee.c.department_id == t.departement.c.id)).\
    group_by(t.employee.c.department_id)
# SELECT "department"."id", "department"."name", avg("employee"."salary") AS "avg_salary" FROM "employee" JOIN "deparment" ON "employee"."department_id" = "departement"."id" GROUP BY "employee"."department_id"


q.insert_into(t.employee[c.name, c.salary, c.department_id]).\
    values(('John Doe', 1000, 1), {'name': 'Jane Doe', 'salary': 2000, 'department_id': 2}).\
    returning(c.id)
# INSERT INTO "employee" ("name", "salary", "department_id") VALUES ('John Doe', 1000, 1), ('Jane Doe', 2000, 2) RETURNING "id"


q.update(t.employee).\
    set((c.salary, c.deparment_id), (3000, 3)).\
    where(c.id == 1)
# UPDATE "employee" SET ("salary", "deparment_id") = (3000, 3) WHERE "id" = 1


q.delete_from(t.employee).\
    where(c.salary > 10000).\
    returning(c.id)
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
