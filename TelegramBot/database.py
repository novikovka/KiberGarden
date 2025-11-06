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

### получение токена теплицы по телеграм айди
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

### получение текущего статуса
async def get_current_status(token, trigger_type):
    query = """
        SELECT status 
        FROM current_state
        WHERE token = $1 AND type = $2
        LIMIT 1;
    """
    row = await pool.fetchrow(query, token, trigger_type)
    return row["status"] if row else None



'''
connection = psycopg2.connect(user="postgres",
                                  password="12345678",
                                  host="localhost",
                                  port="5432")

    cursor = connection.cursor()
'''

