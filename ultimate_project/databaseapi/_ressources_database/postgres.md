# CONNECT TO DB

Run the container in exec mode and run


```bash
# Connect to database in the `database` container
psql -h localhost -p 5432 -U user1 -d transc_db
```
> [!NOTE]
> `user1` refers to the env `POSTGRES_USER` and `transc_db` to `POSTGRES_DB`

```sql
\l -- List databases
```

```sql
\dt -- List tables
```

```sql
\dt user_schema.* -- List tables inside a schema
```

```sql
\d table_name -- Describe table databases
```

``` python
# HOW TO DELETE INLINE
from databaseapi_app.models import Player
result = Player.objects.get(id=13)

Player.objects.get(id=13).delete()
```


```python
from match_app.models import Player, Match

player = Player.objects.first()
print(player)  # ✅ Should return a Player from user_schema.player

match = Match.objects.first()
print(match)  # ✅ Should return a Match from user_schema.match
```




## TESTING POPULATE

```sql
-- Create a table for users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table for products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table for orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);

-- Insert sample data into the users table
INSERT INTO users (username, email) VALUES
('user1', 'user1@example.com'),
('user2', 'user2@example.com'),
('user3', 'user3@example.com');

-- Insert sample data into the products table
INSERT INTO products (name, price) VALUES
('Product A', 19.99),
('Product B', 29.99),
('Product C', 39.99);

-- Insert sample data into the orders table
INSERT INTO orders (user_id, product_id, quantity) VALUES
(1, 1, 2),
(2, 2, 1),
(3, 3, 3);
```

```sql
SELECT * FROM users;
SELECT * FROM products;
SELECT * FROM orders;
```

For deleting all the dummy data

```sql
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;
```