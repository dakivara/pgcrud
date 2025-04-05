
-----

<span style="font-size: 0.9em;">
    **Note**: Make sure to read the [Getting Started](index.md), [Demo Schema](demo-schema.md) and [Cursor](cursor.md) first, as it is essential for better understanding of this tutorial.
</span>

-----

pgcrud has two functions to perform **synchronous** read operations:

- `pg.get_one`: Retrieve a single record. If no record is found, the method returns `None`. If more than one record is found, the method returns the first one.
- `pg.get_many`: Retrieve either a list of records or an iterable cursor.

And pgcrud has two function to perform **asynchronous** read operations:

- `pg.async_get_one`: Analogous to `pg.get_one`.
- `pg.async_get_many`: Analogous to `pg.get_many`.


## Parameters

The following parameters are available:

- `cursor` *(required)*: To execute the query.
- `select` *(required)*: To specify the selected columns.
- `from_` *(required)*: To define the target.[^1]
- `where` *(optional)*: To filter records.
- `group_by` *(optional)*: To group by columns.
- `having` *(optional)*: To filter by aggregated columns.
- `window` *(optional)*: To define windows.
- `order_by` *(optional)*: To sort by columns.
- `limit` *(optional)*: To limit the number of records.[^2]
- `offset` *(optional)*: To skip the first n records.
- `no_fetch` *(optional)*: To execute only.[^2]


[^1]: The only reason why this parameter has a trailing underscore is that `from` is a reserved keyword.

[^2]: Only available in `pg.get_many` and `pg.async_get_many`. 


## Cursor

The `cursor` parameter is explained in detail [here](cursor.md).


## Select

You can use a single expression to select a single column or a sequence of expressions to select multiple columns. [^3]

[^3]: In some cases, you may also want to include constants in your selection. To do this, simply pass the constant value directly in the select statement. Obviously you can also select constants and columns at once.

### Single Column

You use a single expression to select a specific column from a table, accompanied by an appropriate scalar type hint for the cursor.

=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i


    def get_author_name(
            cursor: pg.Cursor, 
            id_: int,
    ) -> str | None:
        
        return pg.get_one(
            cursor=cursor[str],
            select=i.name,
            from_=i.author,
            where=i.id == id_,
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i


    async def get_author_name(
            cursor: pg.AsyncCursor, 
            id_: int,
    ) -> str | None:
        
        return await pg.async_get_one(
            cursor=cursor[str],
            select=i.name,
            from_=i.author,
            where=i.id == id_,
        )
    ```

### Multiple Columns

You use a sequence of expressions to select multiple columns from a table, with the option to fetch the results as a tuple, dictionary, or model instance.


=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i


    def get_book_ids_and_titles(
            cursor: pg.Cursor, 
            author_id: int,
    ) -> tuple[int, str] | None:
        
        return pg.get_many(
            cursor=cursor[tuple[int, str]],
            select=(i.id, i.title),
            from_=i.book,
            where=i.author_id == author_id,
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i


    async def get_book_ids_and_titles(
            cursor: pg.AsyncCursor, 
            author_id: int,
    ) -> tuple[int, str] | None:
        
        return await pg.async_get_many(
            cursor=cursor[tuple[int, str]],
            select=(i.id, i.title),
            from_=i.book,
            where=i.author_id == author_id,
        )
    ```


## From

The `from_` specifies the target. The target is typically a table (or view), joined table, or subquery.


### Table (or View)

You use an expression to select from table (or view).

=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
        
            
    def get_book_ids(cursor: pg.Cursor) -> list[int]:
        return pg.get_many(
            cursor=cursor[int],
            select=i.id,
            from_=i.book,
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
        
            
    async def get_book_ids(cursor: pg.AsyncCursor) -> list[int]:
        return await pg.async_get_many(
            cursor=cursor[int],
            select=i.id,
            from_=i.book,
        )
    ```

### Joined Table

You use a joined expression to select from a joined table. In such a case you will typically load fetched data into data models.

=== "sync"

    ```python
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i, functions as f
    
    
    class Author(BaseModel):
        id: int
        name: str
    
        
    class Book(BaseModel):
        id: int
        title: str
        author: Author
    
    
    def get_book(
            cursor: pg.Cursor,
            id_: int,
    ) -> Book | None:
    
        return pg.get_one(
            cursor=cursor[Book],
            select=(i.book.id, i.book.title, f.to_json(i.author).AS(i.author)),
            from_=i.book.
                JOIN(i.author).ON(i.book.author_id == i.author.id),
            where=i.book.id == id_,
        )
    ```

=== "async"

    ```python
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i, functions as f
    
    
    class Author(BaseModel):
        id: int
        name: str
    
        
    class Book(BaseModel):
        id: int
        title: str
        author: Author
    
    
    async def get_book(
            cursor: pg.AsyncCursor,
            id_: int,
    ) -> Book | None:
    
        return await pg.async_get_one(
            cursor=cursor[Book],
            select=(i.book.id, i.book.title, f.to_json(i.author).AS(i.author)),
            from_=i.book.
                JOIN(i.author).ON(i.book.author_id == i.author.id),
            where=i.book.id == id_,
        )
    ```

## Where

The `where` parameter is used to specify conditions for filtering records to fetch. It 
accepts a comparison expression as its input. This can be a single comparison expression or an 
intersection or union of expressions. 

=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    def get_book_titles(
            cursor: pg.Cursor,
            author_id_1: int,
            author_id_2: int,
    ) -> list[str]:
        
        return pg.get_many(
            cursor=cursor[str],
            select=i.title,
            from_=i.book,
            where=(i.author_id == author_id_1) | (i.author_id == author_id_2),
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    async def get_book_titles(
            cursor: pg.AsyncCursor,
            author_id_1: int,
            author_id_2: int,
    ) -> list[str]:
        
        return await pg.async_get_many(
            cursor=cursor[str],
            select=i.title,
            from_=i.book,
            where=(i.author_id == author_id_1) | (i.author_id == author_id_2),
        )
    ```

### Optional Filter 

It is often convenient to define a function with multiple optional filter parameters. In such cases, you can use `pg.UNDEFINED` as the default 
value. Any comparison expressions involving `pg.UNDEFINED` are automatically excluded from the where condition.

=== "sync"

    ```python
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    class Author(BaseModel):
        id: int
        name: str
    
        
    def get_author(
            cursor: pg.Cursor,
            id_: int | pg.Undefined = pg.UNDEFINED,
            name: str | pg.Undefined = pg.UNDEFINED,
    ) -> Author | None:
    
        return pg.get_one(
            cursor=cursor[Author],
            select=(i.id, i.name),
            from_=i.author,
            where=(i.id == id_) & (i.name == name), 
        )
    ```

=== "async"

    ```python
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    class Author(BaseModel):
        id: int
        name: str
    
        
    async def get_author(
            cursor: pg.AsyncCursor,
            id_: int | pg.Undefined = pg.UNDEFINED,
            name: str | pg.Undefined = pg.UNDEFINED,
    ) -> Author | None:
    
        return await pg.async_get_one(
            cursor=cursor[Author],
            select=(i.id, i.name),
            from_=i.author,
            where=(i.id == id_) & (i.name == name), 
        )
    ```



## Group By

The `group_by` parameter is used to aggregate records based on one or more columns. You can provide a single 
expression to group by one column or multiple expressions to group by several columns.[^4]

[^4]: You can also use pass integers to the `group_by` parameter to group by the respective columns in the `select`clause.

=== "sync"

    ```python
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i, functions as f
    
    
    class AuthorStats(BaseModel):
        author_id: int
        n_books: int
    
        
    def get_author_stats(cursor: pg.Cursor) -> list[AuthorStats]:
        return pg.get_many(
            cursor=cursor[AuthorStats],
            select=(i.author_id, f.count(i.book).AS(i.n_books)),
            from_=i.book,
            group_by=i.author_id,
        )
    ```

=== "async"

    ```python
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i, functions as f
    
    
    class AuthorStats(BaseModel):
        author_id: int
        n_books: int
    
        
    async def get_author_stats(cursor: pg.AsyncCursor) -> list[AuthorStats]:
        return await pg.async_get_many(
            cursor=cursor[AuthorStats],
            select=(i.author_id, f.count(i.book).AS(i.n_books)),
            from_=i.book,
            group_by=i.author_id,
        )
    ```


## Having

The `having` parameter is used to filter records after they have been aggregated with the `group_by` parameter. Similar to 
the `where` parameter, it accepts a comparison expression as input.

=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i, functions as f
    
    
    def get_top_author_ids(
            cursor: pg.Cursor,
            n_books: int,
    ) -> list[int]:
    
        return pg.get_many(
            cursor=cursor[int],
            select=i.author_id,
            from_=i.book,
            group_by=i.author_id,
            having=f.count(i.book) > n_books,
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i, functions as f
    
    
    async def get_top_author_ids(
            cursor: pg.AsyncCursor,
            n_books: int,
    ) -> list[int]:
    
        return await pg.async_get_many(
            cursor=cursor[int],
            select=i.author_id,
            from_=i.book,
            group_by=i.author_id,
            having=f.count(i.book) > n_books,
        )
    ```


## Window

The `window` parameter is used to define windows, which allow calculations across a set of table rows related to the current row. You can 
pass a single or sequence of expressions to the `window` parameter.

=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i, functions as f, QueryBuilder as q

    def get_book_order(cursor: pg.Cursor) -> list[tuple[int, str, int]]:
        return pg.get_many(
            cursor=cursor[tuple[int, str, int]],
            select=(i.author_id, i.title, f.row_number().OVER(i.w)),
            from_=i.book,
            window=i.w.AS(q.PARTITION_BY(i.author_id).ORDER_BY(i.publication_date)),
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i, functions as f, QueryBuilder as q
    
    
    async def get_book_order(cursor: pg.AsyncCursor) -> list[tuple[int, str, int]]:
        return await pg.async_get_many(
            cursor=cursor[tuple[int, str, int]],
            select=(i.author_id, i.title, f.row_number().OVER(i.w)),
            from_=i.book,
            window=i.w.AS(q.ORDER_BY(i.publication_date)),
        )
    ```

## Order By


The `order_by` parameter is used to sort records based on one or more columns. It accepts either a single or a sequence of expressions.


=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    def get_sorted_book_ids(
            cursor: pg.Cursor,
            author_id: int,
    ) -> list[int]:
    
        return pg.get_many(
            cursor=cursor[int],
            select=i.id,
            from_=i.book,
            where=i.author_id == author_id,
            order_by=i.id.ASC(),
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    async def get_sorted_book_ids(
            cursor: pg.AsyncCursor,
            author_id: int,
    ) -> list[int]:
    
        return await pg.async_get_many(
            cursor=cursor[int],
            select=i.id,
            from_=i.book,
            where=i.author_id == author_id,
            order_by=i.id.ASC(),
        )
    ```


### Optional Sort

It is often convenient to define a function with multiple optional sort parameters. In such cases, you can use `pg.UNDEFINED` as the default 
value. Any sort expressions involving `pg.UNDEFINED` are automatically excluded from the `order_by`.



=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import Identifier as i
    
    
    def get_book_ids(
            cursor: pg.Cursor,
            author_id: int,
            id_asc: bool | pg.Undefined = pg.UNDEFINED,
            title_asc: bool | pg.Undefined = pg.UNDEFINED,
    ) -> list[int]:
    
        return pg.get_many(
            cursor=cursor[int],
            select=i.id,
            from_=i.book,
            where=i.author_id == author_id,
            order_by=(i.id.ASC(id_asc), i.title.ASC(title_asc)),
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    async def get_sorted_book_ids(
            cursor: pg.AsyncCursor,
            author_id: int,
            id_asc: bool | pg.Undefined = pg.UNDEFINED,
            title_asc: bool | pg.Undefined = pg.UNDEFINED,
    ) -> list[int]:
    
        return await pg.async_get_many(
            cursor=cursor[int],
            select=i.id,
            from_=i.book,
            where=i.author_id == author_id,
            order_by=(i.id.ASC(id_asc), i.title.ASC(title_asc)),
        )
    ```

## Limit

The `limit` parameter is used to restrict the number of records fetched. It is only available in the `get_many` methods 
and accepts an integer as input.


=== "sync"

    ```python
    from pydantic import BaseModel

    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    class Author(BaseModel):
        id: int
        name: str

    
    def get_authors(
            cursor: pg.Cursor,
            limit: int | None = None,
    ) -> list[Author]:
    
        return pg.get_many(
            cursor=cursor[Author],
            select=(i.id, i.name),
            from_=i.author,
            limit=limit,
        )
    ```

=== "async"

    ```python
    from pydantic import BaseModel

    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    class Author(BaseModel):
        id: int
        name: str

    
    async def get_authors(
            cursor: pg.AsyncCursor,
            limit: int | None = None,
    ) -> list[Author]:
    
        return await pg.async_get_many(
            cursor=cursor[Author],
            select=(i.id, i.name),
            from_=i.author,
            limit=limit,
        )
    ```

## Offset

The `offset` parameter skips a specified number of records in the query result. It is commonly used for pagination or infinite scrolling. It accepts
an integer as input.


=== "sync"

    ```python
    from pydantic import BaseModel

    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    class Author(BaseModel):
        id: int
        name: str

    
    def get_authors(
            cursor: pg.Cursor,
            limit: int | None = None,
            offset: int | None = None,
    ) -> list[Author]:
    
        return pg.get_many(
            cursor=cursor[Author],
            select=(i.id, i.name),
            from_=i.author,
            order_by=i.id,
            limit=limit,
            offset=offset,
        )
    ```

=== "async"

    ```python
    from pydantic import BaseModel

    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    class Author(BaseModel):
        id: int
        name: str

    
    async def get_authors(
            cursor: pg.AsyncCursor,
            limit: int | None = None,
            offset: int | None = None,
    ) -> list[Author]:
    
        return await pg.async_get_many(
            cursor=cursor[Author],
            select=(i.id, i.name),
            from_=i.author,
            order_by=i.id,
            limit=limit,
            offset=offset,
        )
    ```


## No Fetch

The `no_fetch` parameter determines whether to fetch the data or only execute the query. It is only available in the `get_many` methods.
By default, it is set to `False`. If set to `True`, the method will return a cursor, making it more time and memory efficient 
when you need to iterate through the data without loading it all at once.


=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i


    def get_book_titles(cursor: pg.Cursor) -> pg.Cursor[str]:
        return pg.get_many(
            cursor=cursor[str],
            select=i.title,
            from_=i.book,
            no_fetch=True,
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i


    async def get_book_titles(cursor: pg.AsyncCursor) -> pg.AsyncCursor[str]:
        return await pg.async_get_many(
            cursor=cursor[str],
            select=i.title,
            from_=i.book,
            no_fetch=True,
        )
    ```
