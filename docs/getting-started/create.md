-----

<span style="font-size: 0.9em;">
    **Note**: Make sure to read the [Getting Started](index.md), [Demo Schema](demo-schema.md) and [Cursor](cursor.md) first, as it is essential for better understanding of this tutorial.
</span>

-----


pgcrud has two functions to perform **synchronous** insert operations:

- `pg.insert_one`: Insert a single record and optionally return the inserted record.
- `pg.insert_many`: Insert multiple records and optionally return the inserted records or an iterable cursor.

And pgcrud has two function to perform **asynchronous** insert operations:

- `pg.async_insert_one`: Analogous to `pg.insert_one`.
- `pg.async_insert_many`: Analogous to `pg.insert_many`.


## Parameters

The following parameters are available:

- `cursor` *(required)*: To execute the query.
- `insert_into` *(required)*: To specify in which table to insert and which columns to populate.
- `values` *(required)*: The values to insert.
- `on_conflict` *(optional)*: To handle conflicts.
- `returning` *(optional)*: To return the inserted records.
- `additional_values` *(optional)*: Additional values that can be inserted.
- `no_fetch` *(optional)*: To execute only.[^1]


[^1]: Only available in `pg.insert_many` and `pg.async_insert_many`. 


## Cursor

The `cursor` parameter is explained in detail [here](cursor.md).

## Insert Into

The `insert_into` specifies into which table you want to insert and which columns you want to populate. You need to pass 
an identifier or table identifier to this parameter.

=== "sync"

    ```python
    from datetime import date
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    def insert_author(
            cursor: pg.Cursor,
            name: str,
            date_of_birth: date,
    ) -> None:
        
        pg.insert_one(
            cursor=cursor,
            insert_into=i.author[i.name, i.date_of_birth],
            values=(name, date_of_birth),
        )
    ```

=== "async"

    ```python
    from datetime import date
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    async def insert_author(
            cursor: pg.AsyncCursor,
            name: str,
            date_of_birth: date,
    ) -> None:
        
        await pg.async_insert_one(
            cursor=cursor,
            insert_into=i.author[i.name, i.date_of_birth],
            values=(name, date_of_birth),
        )
    ```


## Values

The `values` parameter specifies the records to be inserted into the table. As the names suggest, the `insert_one` method 
inserts a single record and `insert_many` inserts many records.

### Single Record

In the `insert_one` method, the `values` parameter typically expects a tuple, dictionary or model instance.

=== "sync"

    ```python
    from datetime import date
    
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    class AuthorInput(BaseModel):
        name: str
        date_of_birth: date
    
        
    def insert_author(
            cursor: pg.Cursor,
            input_: AuthorInput,
    ) -> None:
        
        pg.insert_one(
            cursor=cursor,
            insert_into=i.author[i.name, i.date_of_birth],
            values=input_,
        )
    ```

=== "async"

    ```python
    from datetime import date
    
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    class AuthorInput(BaseModel):
        name: str
        date_of_birth: date
    
        
    async def insert_author(
            cursor: pg.AsyncCursor,
            input_: AuthorInput,
    ) -> None:
        
        await pg.async_insert_one(
            cursor=cursor,
            insert_into=i.author[i.name, i.date_of_birth],
            values=input_,
        )
    ```


### Multiple Records

In the `insert_many` method, the `values` parameter expects a sequence of tuples, dictionaries or model instance.

=== "sync"

    ```python
    from datetime import date
    
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    class AuthorInput(BaseModel):
        name: str
        date_of_birth: date
    
        
    def insert_authors(
            cursor: pg.Cursor,
            input_: list[AuthorInput],
    ) -> None:
        
        pg.insert_many(
            cursor=cursor,
            insert_into=i.author[i.name, i.date_of_birth],
            values=input_,
        )
    ```

=== "async"

    ```python
    from datetime import date
    
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    class AuthorInput(BaseModel):
        name: str
        date_of_birth: date
    
        
    async def insert_authors(
            cursor: pg.AsyncCursor,
            input_: list[AuthorInput],
    ) -> None:
        
        await pg.async_insert_many(
            cursor=cursor,
            insert_into=i.author[i.name, i.date_of_birth],
            values=input_,
        )
    ```

## On Conflict

The `on_conflict` parameter is used to manage conflicts that arise from constraint violations and 
requires a query as its input.


=== "sync"

    ```python
    from datetime import date
    
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i, QueryBuilder as q
    
    
    class AuthorInput(BaseModel):
        name: str
        date_of_birth: date
    
    
    def insert_author(
            cursor: pg.Cursor,
            input_: AuthorInput,
    ) -> None:
    
        pg.insert_one(
            cursor=cursor,
            insert_into=i.author[i.name, i.date_of_birth],
            values=input_,
            on_conflict=q.ON_CONSTRAINT(i.author_name_key).DO_NOTHING,
        )
    ```


=== "async"

    ```python
    from datetime import date
    
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i, QueryBuilder as q
    
    
    class AuthorInput(BaseModel):
        name: str
        date_of_birth: date
    
    
    async def insert_author(
            cursor: pg.AsyncCursor,
            input_: AuthorInput,
    ) -> None:
    
        await pg.async_insert_one(
            cursor=cursor,
            insert_into=i.author[i.name, i.date_of_birth],
            values=input_,
            on_conflict=q.ON_CONSTRAINT(i.author_name_key).DO_NOTHING,
        )
    ```


## Returning

The `returning` parameter is used to retrieve the record after insertion[^2]. The `returning` parameter 
expects a single or multiple expressions as input.

[^2]: Typically you want to retrieve the autogenerated id.


=== "sync"

    ```python
    from datetime import date
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    def insert_book(
            cursor: pg.Cursor,
            input_: tuple[str, date, int],        
    ) -> int:
        
        return pg.insert_one(
            cursor=cursor[int],
            insert_into=i.book[i.title, i.publication_date, i.author_id],
            values=input_,
            returning=i.id,
        )
    ```

=== "async"

    ```python
    from datetime import date
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    async def insert_book(
            cursor: pg.AsyncCursor,
            input_: tuple[str, date, int],        
    ) -> int:
        
        return await pg.async_insert_one(
            cursor=cursor[int],
            insert_into=i.book[i.title, i.publication_date, i.author_id],
            values=input_,
            returning=i.id,
        )
    ```


## Additional Values

The `additonal_values` parameter is especially useful when the model instance being inserted does not contain all the required 
data. A common example is foreign keys, which may not be part of the model instance but still need to be included in the 
insertion. The `additional_values` expects a dictionary as input.

=== "sync"

    ```python
    from datetime import date
        
    from pydantic import BaseModel
        
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    class BookInput(BaseModel):
        title: str
        publication_date: date
        
        
    class AuthorInput(BaseModel):
        name: str
        date_of_birth: date
        books: list[BookInput]
    
            
    def insert_author_with_books(
            cursor: pg.Cursor,
            input_: AuthorInput,
    ) -> None:
    
        author_id = pg.insert_one(
            cursor[int],
            insert_into=i.author[i.name, i.date_of_birth],
            values=input_,
            returning=i.id,
        )
        
        pg.insert_many(
            cursor=cursor,
            insert_into=i.book[i.title, i.publication_date, i.author_id],
            values=input_.books,
            additional_values={'author_id': author_id},
        ) 
    ```

=== "async"

    ```python
    from datetime import date
        
    from pydantic import BaseModel
        
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    class BookInput(BaseModel):
        title: str
        publication_date: date
        
        
    class AuthorInput(BaseModel):
        name: str
        date_of_birth: date
        books: list[BookInput]
    
            
    async def insert_author_with_books(
            cursor: pg.AsyncCursor,
            input_: AuthorInput,
    ) -> None:
    
        author_id = await pg.async_insert_one(
            cursor[int],
            insert_into=i.author[i.name, i.date_of_birth],
            values=input_,
            returning=i.id,
        )
        
        await pg.async_insert_many(
            cursor=cursor,
            insert_into=i.book[i.title, i.publication_date, i.author_id],
            values=input_.books,
            additional_values={'author_id': author_id},
        ) 
    ```


## No Fetch

The `no_fetch` parameter determines whether to fetch the data or only execute the query. It is only available in the `insert_many` methods.
By default, it is set to `False`. If set to `True`, the method will return a cursor, making it more time and memory efficient 
when you need to iterate through the data without loading it all at once.

=== "sync"

    ```python
    from datetime import date
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    def insert_books(
            cursor: pg.Cursor,
            input_: list[tuple[str, date, int]],        
    ) -> pg.Cursor[int]:
        
        return pg.insert_many(
            cursor=cursor[int],
            insert_into=i.book[i.title, i.publication_date, i.author_id],
            values=input_,
            returning=i.id,
            no_fetch=True,
        )
    ```

=== "async"

    ```python
    from datetime import date
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    async def insert_books(
            cursor: pg.AsyncCursor,
            input_: list[tuple[str, date, int]],        
    ) -> pg.AsyncCursor[int]:
        
        return await pg.async_insert_many(
            cursor=cursor[int],
            insert_into=i.book[i.title, i.publication_date, i.author_id],
            values=input_,
            returning=i.id,
            no_fetch=True,
        )
    ```
