import asyncio
import aiosqlite

DB_NAME = "airbnb.db"

async def asyncfetchusers():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows  # ✅ Must return result

async def asyncfetcholder_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows  # ✅ Must return result

async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        asyncfetchusers(),
        asyncfetcholder_users()
    )

    print("All Users:")
    for user in all_users:
        print(user)

    print("\nUsers older than 40:")
    for user in older_users:
        print(user)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
