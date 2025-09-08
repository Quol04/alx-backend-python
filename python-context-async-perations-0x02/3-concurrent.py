#!/usr/bin/env python3
"""
Run multiple database queries concurrently using asyncio and aiosqlite
"""

import asyncio
import aiosqlite


async def async_fetch_users(db_name="example.db"):
    """Fetch all users from the users table asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows


async def async_fetch_older_users(db_name="example.db"):
    """Fetch users older than 40 from the users table asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            return rows


async def fetch_concurrently():
    """Run both queries concurrently using asyncio.gather."""
    results_all, results_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All Users:")
    for row in results_all:
        print(row)

    print("\nUsers older than 40:")
    for row in results_older:
        print(row)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
