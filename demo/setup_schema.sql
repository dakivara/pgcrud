DROP SCHEMA IF EXISTS demo_schema CASCADE;
CREATE SCHEMA demo_schema;
SET search_path = demo_schema;


CREATE TABLE author (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL UNIQUE,
    date_of_birth date NOT NULL
);


CREATE TABLE book (
    id serial PRIMARY KEY,
    title varchar(255) NOT NULL,
    publication_date date NOT NULL,
    author_id int NOT NULL,
    FOREIGN KEY (author_id) REFERENCES author(id)
);


INSERT INTO author (id, name, date_of_birth) VALUES (1, 'J.K. Rowling', '1965-07-31');
INSERT INTO author (id, name, date_of_birth) VALUES (2, 'George R.R. Martin', '1948-09-20');
INSERT INTO author (id, name, date_of_birth) VALUES (3, 'Dan Brown', '1964-06-22');

INSERT INTO book (id, title, author_id, publication_date) VALUES (1, 'Harry Potter and the Sorcerer''s Stone', 1, '1997-06-26');
INSERT INTO book (id, title, author_id, publication_date) VALUES (2, 'Harry Potter and the Chamber of Secrets', 1, '1998-07-02');
INSERT INTO book (id, title, author_id, publication_date) VALUES (3, 'Harry Potter and the Prisoner of Azkaban', 1, '1999-07-08');

INSERT INTO book (id, title, author_id, publication_date) VALUES (4, 'A Game of Thrones', 2, '1996-08-06');
INSERT INTO book (id, title, author_id, publication_date) VALUES (5, 'A Clash of Kings', 2, '1998-11-16');
INSERT INTO book (id, title, author_id, publication_date) VALUES (6, 'A Storm of Swords', 2, '2000-08-08');

INSERT INTO book (id, title, author_id, publication_date) VALUES (7, 'The Da Vinci Code', 3, '2003-03-18');
INSERT INTO book (id, title, author_id, publication_date) VALUES (8, 'Angels & Demons', 3, '2000-05-01');
INSERT INTO book (id, title, author_id, publication_date) VALUES (9, 'Inferno', 3, '2013-05-14');


SELECT setval('author_id_seq', 4);
SELECT setval('book_id_seq', 10);
