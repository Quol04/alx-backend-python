# #!/usr/bin/env python3
# """
# Run multiple database queries concurrently using asyncio and aiosqlite
# """

# import asyncio
# import aiosqlite


# async def async_fetch_users(db_name: str = "example.db"):
#     """Fetch all users from the users table asynchronously."""
#     async with aiosqlite.connect(db_name) as db:
#         async with db.execute("SELECT * FROM users") as cursor:
#             rows = await cursor.fetchall()
#             return rows


# async def async_fetch_older_users(db_name: str = "example.db"):
#     """Fetch users older than 40 from the users table asynchronously."""
#     async with aiosqlite.connect(db_name) as db:
#         async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
#             rows = await cursor.fetchall()
#             return rows


# async def fetch_concurrently():
#     """Run both queries concurrently using asyncio.gather."""
#     results_all, results_older = await asyncio.gather(
#         async_fetch_users(),
#         async_fetch_older_users()
#     )

#     print("All Users:")
#     for row in results_all:
#         print(row)

#     print("\nUsers older than 40:")
#     for row in results_older:
#         print(row)


# if __name__ == "__main__":
#     asyncio.run(fetch_concurrently())


#!/usr/bin/env python3
"""
Run multiple database queries concurrently using asyncio.gather
"""

import asyncio
import aiosqlite


# Function to fetch all users
async def asyncfetchusers():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows


# Function to fetch users older than 40
async def asyncfetcholder_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows


# Run both queries concurrently
async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        asyncfetchusers(),
        asyncfetcholder_users()
    )
    print("All Users:", users)
    print("Users older than 40:", older_users)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
