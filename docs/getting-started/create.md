-----

<span style="font-size: 0.9em;">
    **Note**: Make sure to read the [Getting Started](index.md), [Demo Schema](demo-schema.md) and [Cursor](cursor.md) first, as it is essential for better understanding of this tutorial.
</span>

-----


pgcrud has two functions to perform **synchronous** insert operations:

- `pg.insert_one`: Insert a single record and optionally return the inserted record.
- `pg.insert_many`: Insert multiple records and optionally return the inserted records or an iterable cursor.

And pgcrud has two function to perform **asynchronous** insert operations:

- `pg.a.insert_one`: Analogous to `pg.insert_one`
- `pg.a.insert_many`: Analogous to `pg.insert_many`


## Parameters

The following parameters are available:

- `cursor` *(required)*: To execute the query.
- `insert_into` *(required)*: To specify in which table to insert and which columns to populate.
- `values` *(required)*: The values to insert.
- `returning` *(optional)*: To return the inserted records.
- `additional_values` *(optional)*: Additional values that can be inserted.


## Cursor

The `cursor` parameter is explained in detail [here](cursor.md).


## Insert Into

The `insert_into` specifies into which table you want to insert and which columns you want to populate. You need to pass a 
table expression to this parameter. A table expression is of the following form: `e.table_name[e.column_name_1, e.column_name_2]`.

=== "sync"

    ```python
    from datetime import date
    
    import pgcrud as pg
    from pgcrud import e
    
    
    def insert_author(
            cursor: pg.Cursor,
            name: str,
            date_of_birth: date,
    ) -> None:
        
        pg.insert_one(
            cursor=cursor,
            insert_into=e.author[e.name, e.date_of_birth],
            values=(name, date_of_birth),
        )
    ```

=== "async"

    ```python
    from datetime import date
    
    import pgcrud as pg
    from pgcrud import e
    
    
    async def insert_author(
            cursor: pg.a.Cursor,
            name: str,
            date_of_birth: date,
    ) -> None:
        
        await pg.a.insert_one(
            cursor=cursor,
            insert_into=e.author[e.name, e.date_of_birth],
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
    from pgcrud import e
    
    
    class AuthorInput(BaseModel):
        name: str
        date_of_birth: date
    
        
    def insert_author(
            cursor: pg.Cursor,
            input_: AuthorInput,
    ) -> None:
        
        pg.insert_one(
            cursor=cursor,
            insert_into=e.author[e.name, e.date_of_birth],
            values=input_,
        )
    ```

=== "async"

    ```python
    from datetime import date
    
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import e
    
    
    class AuthorInput(BaseModel):
        name: str
        date_of_birth: date
    
        
    async def insert_author(
            cursor: pg.a.Cursor,
            input_: AuthorInput,
    ) -> None:
        
        await pg.a.insert_one(
            cursor=cursor,
            insert_into=e.author[e.name, e.date_of_birth],
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
    from pgcrud import e
    
    
    class AuthorInput(BaseModel):
        name: str
        date_of_birth: date
    
        
    def insert_authors(
            cursor: pg.Cursor,
            input_: list[AuthorInput],
    ) -> None:
        
        pg.insert_many(
            cursor=cursor,
            insert_into=e.author[e.name, e.date_of_birth],
            values=input_,
        )
    ```

=== "async"

    ```python
    from datetime import date
    
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import e
    
    
    class AuthorInput(BaseModel):
        name: str
        date_of_birth: date
    
        
    async def insert_authors(
            cursor: pg.a.Cursor,
            input_: list[AuthorInput],
    ) -> None:
        
        await pg.a.insert_many(
            cursor=cursor,
            insert_into=e.author[e.name, e.date_of_birth],
            values=input_,
        )
    ```


## Returning

The `returning` parameter is used to retrieve the record after insertion[^1]. The `returning` parameter 
expects a single or multiple expressions as input.

[^1]: Typically you want to retrieve the autogenerated id.


=== "sync"

    ```python
    from datetime import date
    
    import pgcrud as pg
    from pgcrud import e
    
    
    def insert_book(
            cursor: pg.Cursor,
            input_: tuple[str, date, int],        
    ) -> int:
        
        return pg.insert_one(
            cursor=cursor[int],
            insert_into=e.book[e.title, e.publication_date, e.author_id],
            values=input_,
            returning=e.id,
        )
    ```

=== "async"

    ```python
    from datetime import date
    
    import pgcrud as pg
    from pgcrud import e
    
    
    async def insert_book(
            cursor: pg.a.Cursor,
            input_: tuple[str, date, int],        
    ) -> int:
        
        return await pg.a.insert_one(
            cursor=cursor[int],
            insert_into=e.book[e.title, e.publication_date, e.author_id],
            values=input_,
            returning=e.id,
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
    from pgcrud import e
    
    
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
            insert_into=e.author[e.name, e.date_of_birth],
            values=input_,
            returning=e.id,
        )
        
        pg.insert_many(
            cursor=cursor,
            insert_into=e.book[e.title, e.publication_date, e.author_id],
            values=input_.books,
            additional_values={'author_id': author_id},
        ) 
    ```

=== "async"

    ```python
    from datetime import date
        
    from pydantic import BaseModel
        
    import pgcrud as pg
    from pgcrud import e
    
    
    class BookInput(BaseModel):
        title: str
        publication_date: date
        
        
    class AuthorInput(BaseModel):
        name: str
        date_of_birth: date
        books: list[BookInput]
    
            
    async def insert_author_with_books(
            cursor: pg.a.Cursor,
            input_: AuthorInput,
    ) -> None:
    
        author_id = await pg.a.insert_one(
            cursor[int],
            insert_into=e.author[e.name, e.date_of_birth],
            values=input_,
            returning=e.id,
        )
        
        await pg.a.insert_many(
            cursor=cursor,
            insert_into=e.book[e.title, e.publication_date, e.author_id],
            values=input_.books,
            additional_values={'author_id': author_id},
        ) 
    ```
