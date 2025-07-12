import asyncio
import aiosqlite
import os

DB_NAME = "airbnb.db"

async def setup_database():
    """
    Sets up the SQLite database and populates it with sample data.
    This function ensures the 'users' table exists for the queries.
    """
    # Remove existing DB file to start fresh for demonstration
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Removed existing {DB_NAME}")

    async with aiosqlite.connect(DB_NAME) as db:
        # Create the users table if it doesn't exist
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                city TEXT
            )
        """)
        # Insert some sample data
        await db.execute("INSERT INTO users (name, age, city) VALUES (?, ?, ?)", ("Alice", 30, "New York"))
        await db.execute("INSERT INTO users (name, age, city) VALUES (?, ?, ?)", ("Bob", 45, "Los Angeles"))
        await db.execute("INSERT INTO users (name, age, city) VALUES (?, ?, ?)", ("Charlie", 25, "Chicago"))
        await db.execute("INSERT INTO users (name, age, city) VALUES (?, ?, ?)", ("David", 50, "Houston"))
        await db.execute("INSERT INTO users (name, age, city) VALUES (?, ?, ?)", ("Eve", 35, "Phoenix"))
        await db.execute("INSERT INTO users (name, age, city) VALUES (?, ?, ?)", ("Frank", 60, "Philadelphia"))
        await db.commit()
    print(f"Database {DB_NAME} setup and populated successfully.")

async def asyncfetchusers():
    """
    Fetches all users from the 'users' table.
    Returns a list of tuples, where each tuple represents a user row.
    """
    print("Fetching all users...")
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("Finished fetching all users.")
            return rows

async def asyncfetcholder_users():
    """
    Fetches users older than 40 from the 'users' table.
    Returns a list of tuples, where each tuple represents a user row.
    """
    print("Fetching users older than 40...")
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("Finished fetching users older than 40.")
            return rows

async def fetch_concurrently():
    """
    Executes asyncfetchusers and asyncfetcholder_users concurrently
    and prints their results.
    """
    print("Starting concurrent fetches...")
    all_users, older_users = await asyncio.gather(
        asyncfetchusers(),
        asyncfetcholder_users()
    )
    print("Concurrent fetches completed.")

    print("\n--- All Users ---")
    if all_users:
        for user in all_users:
            print(user)
    else:
        print("No users found.")

    print("\n--- Users older than 40 ---")
    if older_users:
        for user in older_users:
            print(user)
    else:
        print("No users older than 40 found.")

if __name__ == "__main__":
    # Run the database setup and then the concurrent fetch
    async def main():
        await setup_database()
        await fetch_concurrently()

    # Use await main() instead of asyncio.run(main()) in Colab
    syncio.run(main())