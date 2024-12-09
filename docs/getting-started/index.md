
pgcrud is designed to closely mirror PostgreSQL's query language. If you are familiar 
with PostgreSQL, you will quickly recognize the similarities, making this tutorial much easier to follow.

There are 3 key objects in pgcrud which are essential for unlocking its full functionality. The 3 objects are 
named `e`, `f`, and `q` and can be imported using `from pgcrud import e, f, q`.

- Expression Generator `e`: Creates generic references to database objects.
- Function Bearer `f`: Facilitates the use of PostgreSQL functions.
- Query Builder `q`: Enables modular query construction, mirroring PostgreSQL.

## Expression Generator

Any attribute of the Expression Generator is an expression, and any attribute of 
an expression is also an expression[^1]. Expressions are primarily used to 
represent tables or columns in the database.

[^1]: Except for keywords, like `JOIN`, `OVER` or `AS`, which a pre-defined methods of an expression.

```python
from pgcrud import e

e.author
# "author"

e.name
# "name"

e.author.name
# "author"."name"
```

### Arithmetic Operations

Expressions fully support arithmetic operations with each other and with built-in Python objects. 
The result of each operation is again an expression.

```python
from pgcrud import e

e.salary + e.bonus
# "salary" + "bonus"

e.net_price * 1.2
# "net_price" * 1.2

e.weight / e.height ** 2
# "weight" / ("height" ^ 2)
```

### Comparison Operations

Expressions fully support comparison operations with each other and with built-in Python objects. Additionally, you can 
chain them logically using the `&` and `|` operators.

```python
from pgcrud import e

e.author.id == 1
# "author"."id" = 1

e.salary + e.bonus > 10000
# "salary" + "bonus" > 10000

e.id.IN([1, 2, 3])
# "id" IN (1, 2, 3)

(e.age > 4) | (e.height > 100)
# "age" > 4 OR "height" > 100
```

### Reference for Table and Columns

For insert operations, you need to specify the target table and the columns you want to populate.

```python
from pgcrud import e

e.author[e.name, e.date_of_birth]
# "author" ("name", "date_of_birth")
```


### Aliases

You can alias any expression to simplify or make your code clearer.

```python
from pgcrud import e

(e.salary + e.bonus).AS('total_compensation')
# "salary" + "bonus" AS "total_compensation"

(e.weight / e.height ** 2).AS('bmi')
# "weight" / ("height" ^ 2) AS "bmi"
```

### Join Expressions

Expressions support defining joins in a style similar to PostgreSQL. 

```python
from pgcrud import e

e.book.\
    LEFT_JOIN(e.autor).\
    ON(e.book.author_id == e.author.id)
# "book" LEFT JOIN "autor" ON "book"."author_id" = "author"."id"

e.employee.AS('e').\
    JOIN(e.department.AS('d')).\
    ON((e.e.department_id == e.d.id) & (e.d.type == 'Finance'))
# "employee" AS "e" JOIN "department" AS "d" ON "e"."department_id" = "d"."id" AND "d"."type" = 'Finance'
```

## Function Bearer

The Function Bearer encapsulates all PostgreSQL functions, which can be used to transform or aggregate database objects.

```python
from pgcrud import e, f

f.avg(e.salary)
# avg("salary")

f.coalesce(e.score, 0)
# coalesce("score", 0)

f.json_agg(e.book)
# json_agg("book")
```


## Query Builder

The Query Builder is used to chain multiple clauses together to construct an SQL query. You typically use this to 
define windows, subqueries or to construct queries that cannot be achieved using the pre-defined CRUD operations provided by pgcrud.

### Window

You can define windows or use the `OVER` clause.

```python
from pgcrud import e, f, q
from pgcrud.frame_boundaries import UNBOUNDED_PRECEDING, CURRENT_ROW

e.w.AS(
    q.PARTITION_BY(e.product_id).
    ORDER_BY(e.sale_timestamp).
    ROWS_BETWEEN(UNBOUNDED_PRECEDING, CURRENT_ROW)
)
# "w" AS (PARTITION BY "product_id" ORDER BY "sale_timestamp" ROWS BETWEEN UNBOUNDED PRECEEDING AND CURRENT ROW)

(e.salary / f.avg(e.salary)).OVER(q.PARTITION_BY(e.department_id)).AS('relative_salary')
# "salary" / avg("salary") OVER (PARTITION BY "department_id") AS "relative_salary"
```

### Subquery

You can use subqueries in filter expressions or join expressions.

```python
from pgcrud import e, f, q

e.id.IN(
    q.SELECT(e.department_id).
    FROM(e.employee).
    GROUP_BY(e.department_id).
    HAVING(f.avg(e.salary) > 10000)
)
# "id" IN (SELECT "department_id" FROM "employee" GROUP BY "department_id" HAVING avg("salary") > 10000)

e.author.JOIN(
    q.SELECT((e.author_id, f.json_agg(e.book).AS('books'))).
        FROM(e.book).
        GROUP_BY(e.author_id).
        AS('author_books')
    ).ON(e.author.id == e.author_books.author_id)
# "author" JOIN (SELECT "author_id", json_agg("book") AS "books" FROM "book" GROUP BY "author_id") AS "author_books" ON "author"."id" = "author_books"."author_id"
```

### Common Table Expression (CTE)

pgcrud provides pre-defined functions for most relevant CRUD operations but does not cover cases like CTEs. In 
such scenarios, you can use the Query Builder to construct your query.

```python
from pgcrud import e, f, q

q.WITH(
    e.stats.AS(
        q.SELECT((e.department_id, f.avg(e.salary).AS('avg_salary'))).
        FROM(e.employee).
        GROUP_BY(e.department_id)
    )
).INSERT_INTO(e.department_stats[e.id, e.avg_salary]).\
    SELECT((e.department_id, e.avg_salary)).\
    FROM(e.stats)
# WITH "stats" AS (SELECT "department_id", avg("salary") AS "avg_salary" FROM "employee" GROUP BY "department_id") INSERT INTO "department_stats" ("id", "avg_salary") SELECT "department_id", "avg_salary" FROM "stats"


```



