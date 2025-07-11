import asyncio
import aiosqlite

async def async_fetch_users():
    """
    Asynchronous function that fetches all users
    """
    query = "SELECT * FROM users"
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(query) as cursor:
            rows = await cursor.fetchall()
            return rows

async def async_fetch_older_users():
    """
    Asynchronous function that fetches all users older than 40
    """
    query = "SELECT * FROM users WHERE age > ?"
    params = (40,)
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return rows

async def fetch_concurrently():
    """
    Concurrent fetch using asyncio.gather
    """
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    """
    Run the concurrent fetch
    """
    asyncio.run(fetch_concurrently())
