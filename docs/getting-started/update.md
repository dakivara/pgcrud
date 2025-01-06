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

- cursor *(required)*: 
- update *(required)*:
- set_ *(required)*:
- from_ *(optional)*:
- where *(optional)*:
- returning *(optional)*:
- additional_values *(optional)*:
- no_fetch *(optional)*:

## cursor


## Update


## Set


## From


## Where


## Returning


## Additional Values


## No Fetch
