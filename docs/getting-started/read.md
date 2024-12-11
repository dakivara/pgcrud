
-----

<span style="font-size: 0.9em;">
    **Note**: Make sure to read the [Getting Started](index.md) and [Demo Schema](demo-schema.md) first, as it is essential for better understanding of this tutorial.
</span>

-----

pgcrud has two functions to perform **synchronous** read operations:

- `pg.get_one`: Returns a single record. If no record is found, the method returns `None`. If more than one record is found, the method returns the first one.
- `pg.get_many`: Returns either a list of records or an iterable cursor.

And pgcrud has two function to perform **asynchronous** read operations:

- `pg.a.get_one`: Analogous to `pg.get_one`
- `pg.a.get_many`: Analogous to `pg.get_many`


## Parameters


The following parameters are available:

- `cursor`: Cursor / AsyncCursor from `psycopg`
- `select`: To specify the selected columns.
- `from_`: To define the target.[^1]
- `where`: To filter records.
- `group_by`: To group by columns.
- `having`: To filter by aggregated columns.
- `window`: To define windows.
- `order_by`: To sort by columns.
- `limit`: To limit the number of records.[^2]
- `offset`: To skip the first n records.
- `no_fetch`: To execute only.[^2]


[^1]: The only reason why this parameter has a trailing underscore is that `from` is a reserved keyword.

[^2]: Only available in `pg.get_many` and `pg.a.get_many`. 


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

=== "sync"

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
    ```

=== "async"

    ```python
    from psycopg import AsyncCursor
    
    import pgcrud as pg
    from pgcrud import e
    
    
    async def get_author_name(
            cursor: AsyncCursor[str], 
            id_: int,
    ) -> str | None:
        
        return await pg.a.get_one(
            cursor=cursor,
            select=e.name,
            from_=e.author,
            where=e.id == id_,
        )
    ```



### Tuple

Pass a sequence of expressions to the `select` parameter when you want to retrieve multiple columns as a tuple.


=== "sync"

    ```python
    from psycopg import Cursor
    
    import pgcrud as pg
    from pgcrud import e
    
    
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

=== "async"

    ```python
    from psycopg import AsyncCursor
    
    import pgcrud as pg
    from pgcrud import e
    
    
    async def get_book_ids_and_titles(
            cursor: AsyncCursor[tuple[int, str]],
            author_id: int,
    ) -> list[tuple[int, str]]:
        
        return await pg.a.get_many(
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

=== "sync"

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
    ```

=== "async"

    ```python
    from datetime import date
    from typing import Annotated
    
    from psycopg import AsyncCursor
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import e
    
    
    class Author(BaseModel):
        id: int
        name: str
        dob: Annotated[date, e.date_of_birth]
    
    
    async def get_author(
            cursor: AsyncCursor[Author], 
            id_: int,
    ) -> Author | None:
        
        return await pg.a.get_one(
            cursor=cursor,
            select=Author,
            from_=e.author,
            where=e.id == id_,
        )
    ```


## From

The `from_` parameter is required and specifies the target. The target is typically a table, view, joined table, or subquery.

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

