import asyncpg
from typing import Optional

import psycopg2

pool: Optional[asyncpg.Pool] = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(
        user='postgres',
        password='230922',
        database='mybotdb',
        host='127.0.0.1',
        port=5432
    )
    print("✅ Database pool created")


async def close_db():
    global pool
    if pool:
        await pool.close()
        print("🟡 Database pool closed")


async def get_token_by_telegram_id(telegram_id: int):
    global pool
    async with pool.acquire() as conn:
        result = await conn.fetchrow(
            "SELECT token FROM users WHERE telegram_id = $1",
            telegram_id
        )
        if result:
            return result["token"]
        return None




'''
connection = psycopg2.connect(user="postgres",
                                  password="12345678",
                                  host="localhost",
                                  port="5432")

    cursor = connection.cursor()
'''

