
-----

<span style="font-size: 0.9em;">
    **Note**: Make sure to read the [Getting Started](index.md), [Demo Schema](demo-schema.md) and [Cursor](cursor.md) first, as it is essential for better understanding of this tutorial.
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

[^2]: Only available in `pg.get_many` and `pg.a.get_many`. 


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
    from pgcrud import e


    def get_author_name(
            cursor: pg.Cursor, 
            id_: int,
    ) -> str | None:
        
        return pg.get_one(
            cursor=cursor[str],
            select=e.name,
            from_=e.author,
            where=e.id == id_,
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import e


    async def get_author_name(
            cursor: pg.a.Cursor, 
            id_: int,
    ) -> str | None:
        
        return await pg.a.get_one(
            cursor=cursor[str],
            select=e.name,
            from_=e.author,
            where=e.id == id_,
        )
    ```

### Multiple Columns

You use a sequence of expressions to select multiple columns from a table, with the option to fetch the results as a tuple, dictionary, or model instance.


=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import e


    def get_book_ids_and_titles(
            cursor: pg.Cursor, 
            author_id: int,
    ) -> tuple[int, str] | None:
        
        return pg.get_many(
            cursor=cursor[tuple[int, str]],
            select=(e.id, e.title),
            from_=e.book,
            where=e.author_id == author_id,
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import e


    async def get_book_ids_and_titles(
            cursor: pg.a.Cursor, 
            author_id: int,
    ) -> tuple[int, str] | None:
        
        return await pg.a.get_many(
            cursor=cursor[tuple[int, str]],
            select=(e.id, e.title),
            from_=e.book,
            where=e.author_id == author_id,
        )
    ```


## From

The `from_` specifies the target. The target is typically a table (or view), joined table, or subquery.


### Table (or View)

You use an expression to select from table (or view).

=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import e
        
            
    def get_book_ids(cursor: pg.Cursor) -> list[int]:
        return pg.get_many(
            cursor=cursor[int],
            select=e.id,
            from_=e.book,
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import e
        
            
    async def get_book_ids(cursor: pg.a.Cursor) -> list[int]:
        return await pg.a.get_many(
            cursor=cursor[int],
            select=e.id,
            from_=e.book,
        )
    ```

### Joined Table

You use a joined expression to select from a joined table. In such a case you will typically load fetched data into data models.

=== "sync"

    ```python
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import e, f
    
    
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
            select=(e.book.id, e.book.title, f.to_json(e.author).AS('author')),
            from_=e.book.
                JOIN(e.author).ON(e.book.author_id == e.author.id),
            where=e.book.id == id_,
        )
    ```

=== "async"

    ```python
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import e, f
    
    
    class Author(BaseModel):
        id: int
        name: str
    
        
    class Book(BaseModel):
        id: int
        title: str
        author: Author
    
    
    async def get_book(
            cursor: pg.a.Cursor,
            id_: int,
    ) -> Book | None:
    
        return await pg.a.get_one(
            cursor=cursor[Book],
            select=(e.book.id, e.book.title, f.to_json(e.author).AS('author')),
            from_=e.book.
                JOIN(e.author).ON(e.book.author_id == e.author.id),
            where=e.book.id == id_,
        )
    ```

## Where

The `where` parameter expects a comparison expression. This can be a single comparison expression or an intersection or union of expressions. 

=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import e
    
    
    def get_book_titles(
            cursor: pg.Cursor,
            author_id_1: int,
            author_id_2: int,
    ) -> list[str]:
        
        return pg.get_many(
            cursor=cursor[str],
            select=e.title,
            from_=e.book,
            where=(e.author_id == author_id_1) | (e.author_id == author_id_2),
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import e
    
    
    async def get_book_titles(
            cursor: pg.a.Cursor,
            author_id_1: int,
            author_id_2: int,
    ) -> list[str]:
        
        return await pg.a.get_many(
            cursor=cursor[str],
            select=e.title,
            from_=e.book,
            where=(e.author_id == author_id_1) | (e.author_id == author_id_2),
        )
    ```

### Optional Filter 

It is often convenient to define a function with multiple optional filter parameters. In such cases, you can use `pg.Undefined` as the default 
value. Any comparison expressions involving `pg.Undefined` are automatically excluded from the where condition.

=== "sync"

    ```python
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import e
    
    
    class Author(BaseModel):
        id: int
        name: str
    
        
    def get_author(
            cursor: pg.Cursor,
            id_: int | type[pg.Undefined] = pg.Undefined,
            name: str | type[pg.Undefined] = pg.Undefined,
    ) -> Author | None:
    
        return pg.get_one(
            cursor=cursor[Author],
            select=(e.id, e.name),
            from_=e.author,
            where=(e.id == id_) & (e.name == name), 
        )
    ```

=== "async"

    ```python
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import e
    
    
    class Author(BaseModel):
        id: int
        name: str
    
        
    async def get_author(
            cursor: pg.a.Cursor,
            id_: int | type[pg.Undefined] = pg.Undefined,
            name: str | type[pg.Undefined] = pg.Undefined,
    ) -> Author | None:
    
        return await pg.a.get_one(
            cursor=cursor[Author],
            select=(e.id, e.name),
            from_=e.author,
            where=(e.id == id_) & (e.name == name), 
        )
    ```



## Group By

You can pass a single or multiple expressions to group by the corresponding columns.[^4]

[^4]: You can also use pass integers to the `group_by` parameter to group by the respective columns in the `select`clause.

=== "sync"

    ```python
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import e, f
    
    
    class AuthorStats(BaseModel):
        author_id: int
        n_books: int
    
        
    def get_author_stats(cursor: pg.Cursor) -> list[AuthorStats]:
        return pg.get_many(
            cursor=cursor[AuthorStats],
            select=(e.author_id, f.count(e.book).AS('n_books')),
            from_=e.book,
            group_by=e.author_id,
        )
    ```

=== "async"

    ```python
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import e, f
    
    
    class AuthorStats(BaseModel):
        author_id: int
        n_books: int
    
        
    async def get_author_stats(cursor: pg.a.Cursor) -> list[AuthorStats]:
        return await pg.a.get_many(
            cursor=cursor[AuthorStats],
            select=(e.author_id, f.count(e.book).AS('n_books')),
            from_=e.book,
            group_by=e.author_id,
        )
    ```


## Having

Similar to the `where` parameter you can pass a comparison expression to the `having` parameter.

=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import e, f
    
    
    def get_top_author_ids(
            cursor: pg.Cursor,
            n_books: int,
    ) -> list[int]:
    
        return pg.get_many(
            cursor=cursor[int],
            select=e.author_id,
            from_=e.book,
            group_by=e.author_id,
            having=f.count(e.book) > n_books,
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import e, f
    
    
    async def get_top_author_ids(
            cursor: pg.a.Cursor,
            n_books: int,
    ) -> list[int]:
    
        return await pg.a.get_many(
            cursor=cursor[int],
            select=e.author_id,
            from_=e.book,
            group_by=e.author_id,
            having=f.count(e.book) > n_books,
        )
    ```


## Window

You can pass a single or sequence of aliased expressions to the `window` parameter.

=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import e, f, q
    
    
    def get_book_order(
            cursor: pg.Cursor,
            author_id: int,
    ) -> list[tuple[str, int]]:
        
        return pg.get_many(
            cursor=cursor[tuple[str, int]],
            select=(e.title, f.row_number().OVER(e.w)),
            from_=e.book,
            where=e.author_id == author_id,
            window=e.w.AS(q.ORDER_BY(e.publication_date)),
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import e, f, q
    
    
    async def get_book_order(
            cursor: pg.a.Cursor,
            author_id: int,
    ) -> list[tuple[str, int]]:
        
        return await pg.a.get_many(
            cursor=cursor[tuple[str, int]],
            select=(e.title, f.row_number().OVER(e.w)),
            from_=e.book,
            where=e.author_id == author_id,
            window=e.w.AS(q.ORDER_BY(e.publication_date)),
        )
    ```

## Order By


## Limit


## Offset


## No Fetch

