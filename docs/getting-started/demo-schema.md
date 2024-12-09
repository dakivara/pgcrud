
We have set up a demo schema that will be used throughout this tutorial. Be sure to set up the 
demo schema in order to run the code examples with the provided sample data. You can find the 
demo schema [here](https://github.com/dakivara/pgcrud/tree/main/demo/setup_schema.sql).
The demo schema consists of two tables: 

- author:

```sql
CREATE TABLE author (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL
)
```

- book:

```sql
CREATE TABLE book (
    id serial PRIMARY KEY,
    title varchar(255) NOT NULL,
    author_id int NOT NULL,
    FOREIGN KEY (author_id) REFERENCES author(id)
)
```

The schema illustrates a straightforward one-to-many relationship, where the author 
serves as the parent and the books as the children. The [script](https://github.com/dakivara/pgcrud/tree/main/demo/setup_schema.sql) also includes insert 
statements with sample data featuring some of my favorite authors and books:

```sql
INSERT INTO author (id, name) VALUES (1, 'J.K. Rowling');
INSERT INTO author (id, name) VALUES (2, 'George R.R. Martin');
INSERT INTO author (id, name) VALUES (3, 'Dan Brown');

INSERT INTO book (id, title, author_id) VALUES (1, 'Harry Potter and the Sorcerer''s Stone', 1);
INSERT INTO book (id, title, author_id) VALUES (2, 'Harry Potter and the Chamber of Secrets', 1);
INSERT INTO book (id, title, author_id) VALUES (3, 'Harry Potter and the Prisoner of Azkaban', 1);

INSERT INTO book (id, title, author_id) VALUES (4, 'A Game of Thrones', 2);
INSERT INTO book (id, title, author_id) VALUES (5, 'A Clash of Kings', 2);
INSERT INTO book (id, title, author_id) VALUES (6, 'A Storm of Swords', 2);

INSERT INTO book (id, title, author_id) VALUES (7, 'The Da Vinci Code', 3);
INSERT INTO book (id, title, author_id) VALUES (8, 'Angels & Demons', 3);
INSERT INTO book (id, title, author_id) VALUES (9, 'Inferno', 3);
```