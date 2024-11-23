# pgcrud

**pgcrud** is a fast and lightweight library that enables seamless integration between PostgreSQL databases, the psycopg adapter and Pydantic models. 
**pgcrud** simplifies CRUD operations with straightforward, abstractly declarative functions, eliminating the need for ORMs or redundant SQL queries.

## Installation

**pgcrud** is not yet available on PyPI, but you can install it with pip using the following command:

```
pip install git+https://github.com/dakivara/pgcrud.git
```

## Documentation

The **pgcrud** documentation is currently under development. We are working on providing comprehensive guides, examples, and API references to help you get the most out of **pgcrud**.

## Simple Example

```python
import pgcrud as pg
from pgcrud import t, c
import psycopg
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    age: int


class UserInput(BaseModel):
    name: str
    age: int
    
    
conn_str = 'YOUR-CONN-STR'

with psycopg.connect(conn_str) as conn:
    with conn.cursor() as cursor:
   
        # get a list of instances from the 'User' model 
        users = pg.get_many(
            cursor=cursor, 
            select=User,        # Map the result to the Pydantic model 'User'
            from_=t.user,       # Specify to query the 'user' table
            where=c.age > 18,   # Filter: Only include users older than 18
            order_by=c.id,      # Sort the results by the 'id' column
        )

        # insert user and return the user_id
        user_id = pg.insert_one(
            cursor=cursor,
            insert_into=t.user,                     # Specify the target table ("user" table)
            values=UserInput(name='Dan', age=30),   # Data to insert, using a Pydantic model (UserInput)
            returning=c.id,                         # Return the "id" column of the newly inserted row
        )
```

## Some Advanced Features

You can easily chain filter expressions in **pgcrud** using logical operators like & (AND) or | (OR).

```python
from pgcrud import c

(c.age > 18) & (c.age < 60) 
# "age" > 18 AND "age" < 60
```

**pgcrud** allows you to declare arithmetic operations between columns python types.

```python
from pgcrud import c

c.weight / c.height ** 2
# "weight" / ("height" ^ 2)
```


The special **Undefined** object is used to handle optional query parameters. When Undefined is included in an expression, it is ignored during query resolution. This makes it easy to build dynamic queries without writing additional conditional logic.
```python
from pgcrud import c, Undefined

(c.age > 18) & (c.age < Undefined) 
# "age" > 18
```


## Why choose pgcrud?

When building applications with a PostgreSQL backend, most developers either opt for ORMs (like SQLAlchemy or SQLModel) or write 
raw SQL. Both approaches have their upsides and downsides:

- ORMs: While convenient, ORMs map directly to tables, but real-world applications often require modeling relationships. This leads to additional data models and more database requests, increasing complexity and overhead.
- Raw SQL: Writing raw SQL avoids the abstraction but comes with its own challenges, such as repetitive code and difficulty handling optional filters or sorting conditions effectively.

Unlike traditional ORMs, **pgcrud** is a purely abstract declarative module and is not tied to specific database tables. This pure declarative nature makes it far more flexible, allowing developers to model their logic and data flow without rigid constraints. It strikes the perfect balance between writing SQL and Python code. We recommend the following approach to make the most of **pgcrud**:

- **Define your database schema**: Use raw SQL to define tables, views, and other static schema elements.
- **Handle regular CRUD operations with pgcrud**: Combine it with Pydantic for a seamless workflow:
  - **Reading**: Leverage PostgreSQL’s powerful JSON aggregation features to define relationships in views, then model these views in Python using Pydantic.
  - **Writing**: Directly map Pydantic models to database tables for clean and efficient data handling.
- **Complex queries**: For advanced use cases, such as Common Table Expressions (CTEs), stick with raw SQL for maximum flexibility.

This approach balances the strengths of SQL and Python, keeping your backend both simple and powerful, and it will drastically reduce your codebase.


## Type Hints
**pgcrud** offers full support for type hints, making it easier to write and maintain your code with better autocompletion and error checking.

- **Recommended Tool**: We recommend using Pyright as it provides accurate and efficient type inference.
- **For PyCharm Users**: We suggest installing the [Pyright plugin](https://github.com/InSyncWithFoo/pyright-for-pycharm) as the standard PyCharm type checker is generally not great. This plugin ensures that type hints are correctly interpreted and validated.
