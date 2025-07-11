import asyncio
import aiosqlite

async def async_fetch_users():
    query = "SELECT * FROM users"
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(query) as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                print(row)

async def async_fetch_older_users():
    query = "SELECT * FROM users WHERE age > ?"
    params = (40,)
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                print(row)

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())