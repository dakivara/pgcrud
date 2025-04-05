-----

<span style="font-size: 0.9em;">
    **Note**: Make sure to read the [Getting Started](index.md), [Demo Schema](demo-schema.md) and [Cursor](cursor.md) first, as it is essential for better understanding of this tutorial.
</span>

-----

pgcrud has one function to perform **synchronous** update operations:

- `pg.update_many`: Updates multiple records.

And pgcrud has one function to perform **asynchronous** update operations:

- `pg.async_update_many`: Analogous to `pg.update_many`. 

Function for single record updates do not exist because PostgreSQL UPDATE command does not inherently target a single record.


## Parameters

- `cursor` *(required)*: To execute the query. 
- `update` *(required)*: To specify which table to update.
- `set_` *(required)*: To assign new values to columns.
- `from_` *(optional)*: To specify tables for subqueries.
- `where` *(optional)*: To determine which rows to update.
- `returning` *(optional)*: To fetch the updated rows.
- `additional_values` *(optional)*: Additional values that can be updated.
- `no_fetch` *(optional)*: To execute only.[^1]

## Cursor

The `cursor` parameter is explained in detail [here](cursor.md).

## Update

The `update` parameter specifies which table to update. It expects an identifier as input.

=== "sync"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    def update_book(
            cursor: pg.Cursor,
            id_: int,
            title: str,
    ) -> None:
        
        pg.update_many(
            cursor=cursor,
            update=i.book,
            set_=(i.title, title),
            where=i.id == id_, 
        )
    ```

=== "async"

    ```python
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    async def update_book(
            cursor: pg.AsyncCursor,
            id_: int,
            title: str,
    ) -> None:
        
        await pg.async_update_many(
            cursor=cursor,
            update=i.book,
            set_=(i.title, title),
            where=i.id == id_, 
        )
    ```

## Set

The `set` parameter expects a tuple containing two items: the first item is either a single identifier or a sequence of identifiers 
that specify the columns to be updated, while the second item can be a single value, a sequence of values, or a model instance.

=== "sync"

    ```python
    from datetime import date
    
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    class AuthorUpdate(BaseModel):
        name: str
        date_of_birth: date
    
    
    def update_author(
            cursor: pg.Cursor,
            id_: int,
            update: AuthorUpdate,
    ) -> None:
            
            pg.update_many(
                cursor=cursor,
                update=i.book,
                set_=((i.name, i.date_of_birth), update),
                where=i.id == id_, 
            )
    ```

=== "async"

    ```python
    from datetime import date
    
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    class AuthorUpdate(BaseModel):
        name: str
        date_of_birth: date
    
    
    async def update_author(
            cursor: pg.AsyncCursor,
            id_: int,
            update: AuthorUpdate,
    ) -> None:
            
            await pg.async_update_many(
                cursor=cursor,
                update=i.book,
                set_=((i.name, i.date_of_birth), update),
                where=i.id == id_, 
            )
    ```

## From


## Where

The `where` parameter is used to specify conditions for updating records. It 
accepts a comparison expression as its input. This can be a single comparison expression or an 
intersection or union of expressions. 

=== "sync"

    ```python
    from datetime import date
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    def update_book(
            cursor: pg.Cursor,
            author_id: int,
            title: str,
            publication_date: date,
    ):
        
        pg.update_many(
            cursor=cursor,
            update=i.book,
            set_=(i.publication_date, publication_date),
            where=(i.title == title) & (i.author_id == author_id),
        )
    ```

=== "async"

    ```python
    from datetime import date
    
    import pgcrud as pg
    from pgcrud import IdentifierExpression as i
    
    
    async def update_book(
            cursor: pg.AsyncCursor,
            author_id: int,
            title: str,
            publication_date: date,
    ):
        
        await pg.async_update_many(
            cursor=cursor,
            update=i.book,
            set_=(i.publication_date, publication_date),
            where=(i.title == title) & (i.author_id == author_id),
        )
    ```

## Returning

The `returning` parameter is used to retrieve the record after update. The `returning` parameter 
expects a single or multiple expressions as input.

## Additional Values


## No Fetch
