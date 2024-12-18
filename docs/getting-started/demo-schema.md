
We have set up a demo schema that will be used throughout this tutorial. Be sure to set up the 
demo schema in order to run the code examples with the provided sample data. You can find the 
demo schema [here](https://github.com/dakivara/pgcrud/tree/main/demo/setup_schema.sql).
The demo schema consists of two tables: 

- author:

```sql
CREATE TABLE author (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL,
    date_of_birth date NOT NULL
)
```

- book:

```sql
CREATE TABLE book (
    id serial PRIMARY KEY,
    title varchar(255) NOT NULL,
    publication_date date NOT NULL,
    author_id int NOT NULL,
    FOREIGN KEY (author_id) REFERENCES author(id)
)
```

The schema illustrates a straightforward one-to-many relationship, where the author 
serves as the parent and the books as the children. The [script](https://github.com/dakivara/pgcrud/tree/main/demo/setup_schema.sql) also includes insert 
statements with sample data featuring some of my favorite authors and books.
