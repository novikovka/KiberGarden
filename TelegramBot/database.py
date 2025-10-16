import asyncpg
from typing import Optional

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
