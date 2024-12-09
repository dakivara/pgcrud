DROP SCHEMA IF EXISTS demo_schema CASCADE;
CREATE SCHEMA demo_schema;
SET search_path = demo_schema;


CREATE TABLE author (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL,
    date_of_birth date NOT NULL
);


CREATE TABLE book (
    id serial PRIMARY KEY,
    title varchar(255) NOT NULL,
    author_id int NOT NULL,
    FOREIGN KEY (author_id) REFERENCES author(id)
);


INSERT INTO author (id, name, date_of_birth) VALUES (1, 'J.K. Rowling', '1965-07-31');
INSERT INTO author (id, name, date_of_birth) VALUES (2, 'George R.R. Martin', '1948-09-20');
INSERT INTO author (id, name, date_of_birth) VALUES (3, 'Dan Brown', '1964-06-22');

INSERT INTO book (id, title, author_id) VALUES (1, 'Harry Potter and the Sorcerer''s Stone', 1);
INSERT INTO book (id, title, author_id) VALUES (2, 'Harry Potter and the Chamber of Secrets', 1);
INSERT INTO book (id, title, author_id) VALUES (3, 'Harry Potter and the Prisoner of Azkaban', 1);

INSERT INTO book (id, title, author_id) VALUES (4, 'A Game of Thrones', 2);
INSERT INTO book (id, title, author_id) VALUES (5, 'A Clash of Kings', 2);
INSERT INTO book (id, title, author_id) VALUES (6, 'A Storm of Swords', 2);

INSERT INTO book (id, title, author_id) VALUES (7, 'The Da Vinci Code', 3);
INSERT INTO book (id, title, author_id) VALUES (8, 'Angels & Demons', 3);
INSERT INTO book (id, title, author_id) VALUES (9, 'Inferno', 3);
