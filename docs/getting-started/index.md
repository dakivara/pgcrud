
pgcrud is designed to closely mirror PostgreSQL's query language. If you are familiar 
with PostgreSQL, you will quickly recognize the similarities, making this tutorial much easier to follow.

There are 3 components in pgcrud which are essential for unlocking its full functionality.

- Expressions: Represent database objects.
- Functions: Facilitates the use of PostgreSQL functions.
- Query Builder: Enables modular query construction, mirroring PostgreSQL.

## Expressions

Expressions represents database objects such as columns, tables, or 
values like integers, text, booleans, and similar types.

### Identifiers

An identifier represents a database object, such as a column, table, or other entity. Any 
attribute of the identifier class is an identifier and any attribute of an identifier is 
again an identifier[^1]. 

[^1]: Except for keywords, like `JOIN`, `OVER` or `AS`, which a pre-defined methods of an expression.

```python
from pgcrud import IdentifierExpression as i

i.author
# "author"

i.name
# "name"

i.author.name
# "author"."name"
```

### Literals

The Literal class is used to convert Python built-in types into PostgreSQL data types..

```python
from datetime import datetime

from pgcrud import LiteralExpression as l

l(1)
# 1

l(datetime.now())
# '2025-01-12 15:59:10.179785'::timestamp

l([1, 2, 3])
# '{1,2,3}'::int2[]
```


### Arithmetic Operations

Expressions fully support arithmetic operations with each other and with built-in Python objects. [^2] 

[^2]: Built in types are automatically converted to literals.


```python
from pgcrud import IdentifierExpression as i

i.salary + i.bonus
# "salary" + "bonus"

i.net_price * 1.2
# "net_price" * 1.2

i.weight / i.height ** 2
# "weight" / ("height" ^ 2)
```

### Comparison Operations

Expressions fully support comparison operations with each other and with built-in Python objects. Additionally, you can 
chain them logically using the `&` and `|` operators.

```python
from pgcrud import IdentifierExpression as i

i.author.id == 1
# "author"."id" = 1

i.salary + i.bonus > 10000
# "salary" + "bonus" > 10000

i.id.IN(1, 2, 3)
# "id" IN (1, 2, 3)

(i.age > 4) | (i.height > 100)
# "age" > 4 OR "height" > 100
```

### Sort Operations

Each expression can specify the ordering of data in either ascending or descending order, with the option to reverse the order using a boolean flag.

```python
from pgcrud import IdentifierExpression as i

i.id.ASC()
# "id" ASC

i.name.DESC()
# "name" DESC

i.id.ASC(False)
# "id" DESC

i.name.DESC(False)
# "name" ASC
```


### Table identifier

For insert operations, you need to specify the target table and the columns you want to populate.

```python
from pgcrud import IdentifierExpression as i

i.author[i.name, i.date_of_birth]
# "author" ("name", "date_of_birth")
```


### Aliases

You can alias any expression to simplify or make your code clearer.

```python
from pgcrud import IdentifierExpression as i

(i.salary + i.bonus).AS(i.total_compensation)
# "salary" + "bonus" AS "total_compensation"

(i.weight / i.height ** 2).AS(i.bmi)
# "weight" / ("height" ^ 2) AS "bmi"
```

### Join Expressions

Expressions support defining joins in a style similar to PostgreSQL. 

```python
from pgcrud import IdentifierExpression as i

i.book \
    .LEFT_JOIN(i.autor) \
    .ON(i.book.author_id == i.author.id)
# "book" LEFT JOIN "autor" ON "book"."author_id" = "author"."id"

i.employee.AS(i.e) \
    .JOIN(i.department.AS(i.d)) \
    .ON((i.e.department_id == i.d.id) & (i.d.type == 'Finance'))
# "employee" AS "e" JOIN "department" AS "d" ON "e"."department_id" = "d"."id" AND "d"."type" = 'Finance'
```

### Undefined Type

pgcrud includes a special object called `pg.UNDEFINED`. When used in comparison or sorting operations, it is automatically ignored. This 
feature is particularly useful for handling optional parameters.

```python
import pgcrud as pg
from pgcrud import IdentifierExpression as i

(i.id == 1) & (i.name == pg.UNDEFINED)
# "id" = 1

i.id.ASC(pg.UNDEFINED)
#
```


## Functions

The Function Bearer encapsulates all PostgreSQL functions, which can be used to transform or aggregate database objects.

```python
from pgcrud import functions as f, IdentifierExpression as i

f.avg(i.salary)
# avg("salary")

f.coalesce(i.score, 0)
# coalesce("score", 0)

f.json_agg(i.book)
# json_agg("book")
```


## Query Builder

The Query Builder is used to chain multiple clauses together to construct an SQL query. You typically use this to 
define windows, subqueries or to construct queries that cannot be achieved using the pre-defined CRUD operations provided by pgcrud.

### Window

You can define windows or use the `OVER` clause.

```python
import pgcrud as pg
from pgcrud import functions as f, IdentifierExpression as i, QueryBuilder as q

i.w.AS(
    q.PARTITION_BY(i.product_id).
    ORDER_BY(i.sale_timestamp).
    ROWS_BETWEEN(pg.UNBOUNDED.PRECEDING, pg.CURRENT_ROW)
)
# "w" AS (PARTITION BY "product_id" ORDER BY "sale_timestamp" ROWS BETWEEN UNBOUNDED PRECEDING CURRENT ROW)

(i.salary / f.avg(i.salary)).OVER(q.PARTITION_BY(i.department_id)).AS(i.relative_salary)
# "salary" / avg("salary") OVER (PARTITION BY "department_id") AS "relative_salary"
```

### Subquery

You can use subqueries in filter expressions or join expressions.

```python
from pgcrud import functions as f, IdentifierExpression as i, QueryBuilder as q

i.id.IN(
    q.SELECT(i.department_id).
    FROM(i.employee).
    GROUP_BY(i.department_id).
    HAVING(f.avg(i.salary) > 10000)
)
# "id" IN ((SELECT "department_id" FROM "employee" GROUP BY "department_id" HAVING avg("salary") > 10000))

i.author.JOIN(
    q.SELECT(i.author_id, f.json_agg(i.book).AS(i.books)).
        FROM(i.book).
        GROUP_BY(i.author_id).
        AS(i.author_books)
    ).ON(i.author.id == i.author_books.author_id)
# "author" JOIN (SELECT "author_id", json_agg("book") AS "books" FROM "book" GROUP BY "author_id") AS "author_books" ON "author"."id" = "author_books"."author_id"
```

### Common Table Expression (CTE)

pgcrud provides pre-defined functions for most relevant CRUD operations but does not cover cases like CTEs. In 
such scenarios, you can use the Query Builder to construct your query.

```python
from pgcrud import functions as f, IdentifierExpression as i, QueryBuilder as q

q.WITH(
    i.stats.AS(
        q.SELECT(i.department_id, f.avg(i.salary).AS(i.avg_salary)).
        FROM(i.employee).
        GROUP_BY(i.department_id)
    )
).INSERT_INTO(i.department_stats[i.id, i.avg_salary]) \
    .SELECT(i.department_id, i.avg_salary) \
    .FROM(i.stats)
# WITH "stats" AS (SELECT "department_id", avg("salary") AS "avg_salary" FROM "employee" GROUP BY "department_id") INSERT INTO "department_stats" ("id", "avg_salary") SELECT "department_id", "avg_salary" FROM "stats"
```
