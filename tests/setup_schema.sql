
CREATE TABLE customer (
    id serial PRIMARY KEY,
    name varchar(255)
);


CREATE TABLE account (
    id serial PRIMARY KEY,
    balance numeric NOT NULL,
    customer_id int NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(id)
);


CREATE TABLE transaction (
    id serial PRIMARY KEY,
    amount numeric NOT NULL,
    created_at timestamp NOT NULL,
    account_id int NOT NULL,
    FOREIGN KEY (account_id) REFERENCES account(id)
);


INSERT INTO customer (id, name) VALUES (1, 'Customer A');
INSERT INTO customer (id, name) VALUES (2, 'Customer B');

INSERT INTO account (id, balance, customer_id) VALUES (1, 1000, 1);
INSERT INTO account (id, balance, customer_id) VALUES (2, 2000, 1);
INSERT INTO account (id, balance, customer_id) VALUES (3, 3000, 1);
INSERT INTO account (id, balance, customer_id) VALUES (4, 1000, 2);
INSERT INTO account (id, balance, customer_id) VALUES (5, 2000, 2);

INSERT INTO transaction (id, amount, created_at, account_id) VALUES (1, 100, TIMESTAMP '2024-01-01 00:11:53', 1);
INSERT INTO transaction (id, amount, created_at, account_id) VALUES (2, 50, TIMESTAMP '2024-01-01 01:24:38', 2);
INSERT INTO transaction (id, amount, created_at, account_id) VALUES (3, 30, TIMESTAMP '2024-01-01 04:57:31', 3);
INSERT INTO transaction (id, amount, created_at, account_id) VALUES (4, 200, TIMESTAMP '2024-01-01 05:23:52', 5);
INSERT INTO transaction (id, amount, created_at, account_id) VALUES (5, 100, TIMESTAMP '2024-01-01 08:45:42', 1);
INSERT INTO transaction (id, amount, created_at, account_id) VALUES (6, 300, TIMESTAMP '2024-01-01 09:50:19', 2);
INSERT INTO transaction (id, amount, created_at, account_id) VALUES (7, 80, TIMESTAMP '2024-01-01 17:19:20', 5);
INSERT INTO transaction (id, amount, created_at, account_id) VALUES (8, 150, TIMESTAMP '2024-01-01 18:06:14', 2);
INSERT INTO transaction (id, amount, created_at, account_id) VALUES (9, 120, TIMESTAMP '2024-01-02 01:09:43', 3);
INSERT INTO transaction (id, amount, created_at, account_id) VALUES (10, 130, TIMESTAMP '2024-01-02 02:46:36', 1);
INSERT INTO transaction (id, amount, created_at, account_id) VALUES (11, 100, TIMESTAMP '2024-01-02 06:55:13', 2);
INSERT INTO transaction (id, amount, created_at, account_id) VALUES (12, 90, TIMESTAMP '2024-01-02 07:00:09', 3);
INSERT INTO transaction (id, amount, created_at, account_id) VALUES (13, 20, TIMESTAMP '2024-01-02 07:41:00', 5);
INSERT INTO transaction (id, amount, created_at, account_id) VALUES (14, 50, TIMESTAMP '2024-01-02 20:15:24', 1);
INSERT INTO transaction (id, amount, created_at, account_id) VALUES (15, 160, TIMESTAMP '2024-01-02 22:53:53', 2);
