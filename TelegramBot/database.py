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

 ### получение телеграм айди по токену
async def get_telegram_id_by_token(token: str):
    global pool
    async with pool.acquire() as conn:
        result = await conn.fetchrow(
            "SELECT telegram_id FROM users WHERE token = $1",
            token
        )
        if result:
            return result["telegram_id"]
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

# получение названия растения, которое выращивает пользователь
async def get_user_plant_name(user_id: int) -> str:
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT plant_name FROM users WHERE telegram_id = $1",
            user_id
        )
    return row["plant_name"] if row and row["plant_name"] else "растение"


### получение суточных данных датчиков по типу
async def get_sensor_data(token: str, sensor_type: str):
    query = """
        SELECT time, value
        FROM sensor_data
        WHERE token = $1 AND type = $2
        ORDER BY time ASC
    """
    async with pool.acquire() as conn:
        rows = await conn.fetch(query, token, sensor_type)

    times = [row["time"] for row in rows]
    values = [float(row["value"]) for row in rows]
    return times, values



'''
connection = psycopg2.connect(user="postgres",
                                  password="12345678",
                                  host="localhost",
                                  port="5432")

    cursor = connection.cursor()
'''

