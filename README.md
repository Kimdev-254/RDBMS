# Mini RDBMS (Pesapal JDEV26 Challenge)

This project is a **simple in-memory relational database management system (RDBMS)** implemented from scratch in Python.  
It supports a subset of SQL, basic indexing, and INNER JOINs, exposed through an interactive REPL.

The goal is **not** to compete with production databases, but to demonstrate clear thinking, core database concepts, and the ability to design systems from first principles.

---

## Features

### Core
- SQL-like interface
- Interactive REPL
- In-memory storage
- Deterministic execution

### Supported SQL
- `CREATE TABLE`
- `INSERT INTO`
- `SELECT *`
- `SELECT * ... WHERE`
- `INNER JOIN`

### Constraints & Indexing
- Primary key enforcement
- Unique column constraints
- Automatic hash-based indexes
- Indexed SELECT and JOIN execution when possible

---

## Example Usage

```sql
CREATE TABLE users (
  id INT PRIMARY KEY,
  name TEXT
);

CREATE TABLE orders (
  id INT PRIMARY KEY,
  user_id INT,
  product TEXT
);

INSERT INTO users VALUES (1, 'Alice');
INSERT INTO users VALUES (2, 'Bob');

INSERT INTO orders VALUES (101, 1, 'Laptop');
INSERT INTO orders VALUES (102, 2, 'Mouse');

SELECT * FROM orders JOIN users ON orders.user_id = users.id;
