import asyncio
import aiosqlite

# Asynchronous function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All Users:")
            for user in users:
                print(user)
            return users

# Asynchronous function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("\nUsers older than 40:")
            for user in older_users:
                print(user)
            return older_users

# Function to run both queries concurrently
async def fetch_concurrently():
    # Run both database queries at the same time
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

# Run the concurrent fetch
asyncio.run(fetch_concurrently())
