The pgcrud cursor extends the psycopg cursor, offering enhanced functionality and usability:

- **Row Factory Integration**: Supports passing a row factory directly via type hints.
- **Built-in Serialization & Validation**: Provides integration with your preferred data serialization and validation library.
- **Execute Queries for Query Builder**: You can directly execute your queries from the pgcrud Query Builder.


## Row Factory

You can use a type hint square brackets on a cursor and pgcrud will choose the appropriate row factory.

=== "sync"

    ```python
    import pgcrud as pg

    
    with pg.connect('CONN_STR') as conn:
        with conn.cursor() as cursor:
            cursor[int].execute("SELECT 1").fetchone()
            # returns 1
    
            cursor[tuple].execute("SELECT 1, 'J.K. Rowling'").fetchone()
            # returns (1, 'J.K. Rowling')

            cursor[list].execute("SELECT 1, 'J.K. Rowling'").fetchone()
            # returns [1, 'J.K. Rowling']

            cursor[dict].execute("SELECT 1 AS id, 'J.K. Rowling' AS name").fetchone()
            # returns {'id': 1, 'name': 'J.K. Rowling'}
    ```

=== "async"

    ```python
    import asyncio    
 
    import pgcrud as pg

    
    async def main():
        async with await pg.async_connect('CONN_STR') as conn:
            async with conn.cursor() as cursor:
                await cursor[int].execute("SELECT 1")
                await cursor.fetchone()
                # returns 1
        
                await cursor[tuple].execute("SELECT 1, 'J.K. Rowling'")
                await cursor.fetchone()
                # returns (1, 'J.K. Rowling')

                await cursor[list].execute("SELECT 1, 'J.K. Rowling'")
                await cursor.fetchone()
                # returns [1, 'J.K. Rowling']

                await cursor[dict].execute("SELECT 1 AS id, 'J.K. Rowling' AS name")
                await cursor.fetchone()
                # returns {'id': 1, 'name': 'J.K. Rowling'}
    

    asyncio.run(main())
    ```

You can provide more detailed type hints, but pgcrud does not perform additional data validation.[^1] Since the database already 
enforces type safety, it is often unnecessary to revalidate types in Python, especially when performance is critical.

[^1]: Unless you have one of the supported validation libraries installed.


=== "sync"

    ```python
    from typing import TypedDict

    import pgcrud as pg


    class Author(TypedDict):
        id: int
        name: str
    

    with pg.connect('CONN_STR') as conn:
        with conn.cursor() as cursor:
            cursor[tuple[int, str]].execute("SELECT 1, 'J.K. Rowling'").fetchone()
            # returns (1, 'J.K. Rowling')

            cursor[Author].execute("SELECT 1 AS id, 'J.K. Rowling' AS name").fetchone()
            # returns {'id': 1, 'name': 'J.K. Rowling'}
    ```

=== "async"

    ```python
    import asyncio 
    from typing import TypedDict

    import pgcrud as pg


    class Author(TypedDict):
        id: int
        name: str
    

    async def main():
        async with await pg.async_connect('CONN_STR') as conn:
            async with conn.cursor() as cursor:
                await cursor[tuple[int, str]].execute("SELECT 1, 'J.K. Rowling'")
                await cursor.fetchone()
                # returns (1, 'J.K. Rowling')

                await cursor[Author].execute("SELECT 1 AS id, 'J.K. Rowling' AS name")
                await cursor.fetchone()
                # returns {'id': 1, 'name': 'J.K. Rowling'}


    asyncio.run(main())
    ```


## Serialization & Validation 

pgcrud currently supports the following data serialization & validation libraries:

- [pydantic](https://docs.pydantic.dev/latest/): the most popular library.
- [msgspec](https://jcristharif.com/msgspec/): the fastest library.

If one of the two libraries is installed, pgcrud will automatically use it for validation.[^2] You can use model instances both to 
determine the row factory and as input parameters.

=== "sync"

    ```python
    from pydantic import BaseModel

    import pgcrud as pg


    class Author(BaseModel):
        id: int
        name: str
    

    with pg.connect('CONN_STR') as conn:
        with conn.cursor() as cursor:
            cursor[tuple[int, str]].execute(
                query="SELECT %(id)s, %(name)s", 
                params=Author(id=1, name='J.K. Rowling'),
            ).fetchone()
            # returns (1, 'J.K. Rowling')
    
            cursor[Author].execute("SELECT 1 AS id, 'J.K. Rowling' AS name").fetchone()
            # returns Author(id=1 name='J.K. Rowling')

            cursor[str].execute("SELECT 1").fetchone()
            # raises ValidationError: Input should be a valid string [type=string_type, input_value=1, input_type=int]
    ```

=== "async"

    ```python
    import asyncio 

    from pydantic import BaseModel

    import pgcrud as pg


    class Author(BaseModel):
        id: int
        name: str
    

    async def main():
        async with await pg.async_connect('CONN_STR') as conn:
            async with conn.cursor() as cursor:
                await cursor[tuple[int, str]].execute(
                    query="SELECT %(id)s, %(name)s", 
                    params=Author(id=1, name='J.K. Rowling'),
                )
                await cursor.fetchone()
                # returns (1, 'J.K. Rowling')
    
                await cursor[Author].execute("SELECT 1 AS id, 'J.K. Rowling' AS name")
                await cursor.fetchone()
                # returns Author(id=1 name='J.K. Rowling')

                await cursor[str].execute("SELECT 1")
                await cursor.fetchone()
                # raises ValidationError: Input should be a valid string [type=string_type, input_value=1, input_type=int]


    asyncio.run(main())
    ```


[^2]: If both libraries are installed, pgcrud will use pydantic by default. You can change it by changing the value of `pg.config.validation`.


## Queries from Query Builder

You can pass a Query from the Query Builder just like a normal SQL query.


=== "sync"

    ```python
    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import Identifier as i, QueryBuilder as q
    
    
    class Author(BaseModel):
        id: int
        name: str
    
    
    with pg.connect('CONN_STR') as conn:
        with conn.cursor() as cursor:
            cursor[Author].execute(
                query=q.SELECT(
                    pg.Placeholder().AS(i.id), 
                    pg.Placeholder().AS(i.name),
                ), 
                params=(1, 'J.K. Rowling'),
            ).fetchone()
            # returns Author(id=1 name='J.K. Rowling')
    
            cursor[tuple[int, str]].execute(
                query=q.SELECT(
                    pg.Placeholder('id'), 
                    pg.Placeholder('name'),
                ), 
                params=Author(id=1, name='J.K. Rowling'),
            ).fetchone()
            # returns (1, 'J.K. Rowling')
    ```

=== "async"

    ```python
    import asyncio

    from pydantic import BaseModel
    
    import pgcrud as pg
    from pgcrud import Identifier as i, QueryBuilder as q
    
    
    class Author(BaseModel):
        id: int
        name: str
    
    
    async def main():
        async with await pg.async_connect('CONN_STR') as conn:
            async with conn.cursor() as cursor:
                await cursor[Author].execute(
                    query=q.SELECT(
                        pg.Placeholder().AS(i.id), 
                        pg.Placeholder().AS(i.name),
                    ), 
                    params=(1, 'J.K. Rowling'),
                )
                await cursor.fetchone()
                # returns Author(id=1 name='J.K. Rowling')
        
                await cursor[tuple[int, str]].execute(
                    query=q.SELECT(
                        pg.Placeholder('id'), 
                        pg.Placeholder('name'),
                    ), 
                    params=Author(id=1, name='J.K. Rowling'),
                )
                await cursor.fetchone()
                # returns (1, 'J.K. Rowling')

    asyncio.run(main())
    ```
