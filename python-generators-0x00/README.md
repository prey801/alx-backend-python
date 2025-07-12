# ALX MySQL User Data Seeder

A Python project to create and populate a MySQL (MariaDB) database with user data from a CSV file.

---

## Features

- Connects to a local MySQL/MariaDB server
- Creates a database named `ALX_prodev`
- Creates a `user_data` table with:
    - `user_id` (UUID, Primary Key)
    - `name` (VARCHAR, NOT NULL)
    - `email` (VARCHAR, NOT NULL)
    - `age` (DECIMAL, NOT NULL)
- Automatically generates UUIDs for each user
- Imports data from `user_data.csv`
- Prints the first 5 rows from the table

---

## Project Structure

```
alx-backend-python/
└── python-generators-0x00/
        ├── main.py         # Main script to run everything
        ├── seed.py         # Handles DB logic and CSV import
        └── user_data.csv   # CSV file with sample user data
```

---

## Requirements

- Python 3.x
- MySQL or MariaDB server
- `mysql-connector-python` package

Install the MySQL connector:

```bash
pip install mysql-connector-python
```

---

## Running the Project

1. Ensure your MySQL/MariaDB server is running.
2. Open a terminal and navigate to the project folder:

        ```bash
        cd python-generators-0x00
        ```

3. Run the script:

        ```bash
        python main.py
        ```

---

## Example CSV (`user_data.csv`)

```csv
name,email,age
Johnnie Mayer,Ross.Reynolds21@hotmail.com,35
Myrtle Waters,Edmund_Funk@gmail.com,99
Flora Rodriguez I,Willie.Bogisich@gmail.com,84
```

> You don't need to include `user_id` — the script generates it automatically.

---

## Database Credentials

Credentials are defined in `seed.py`:

```python
user = "alx_user"
password = "StrongP@ssw0rd!"
host = "localhost"
```

Update these if needed to match your local setup.

---

## Output Example

```
Connected to MySQL server.
Connected to ALX_prodev database.
Data inserted successfully.
✅ Database ALX_prodev is present.
('3fa85f64-5717-4562-b3fc-2c963f66afa6', 'Johnnie Mayer', 'Ross.Reynolds21@hotmail.com', Decimal('35'))
...
```
