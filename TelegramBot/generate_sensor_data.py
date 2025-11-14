import asyncio
import random
from datetime import datetime, timedelta
import asyncpg

async def fill_sensor_data():
    # Подключаемся к базе данных
    conn = await asyncpg.connect(
        user='postgres',
        password='230922',
        database='mybotdb',
        host='127.0.0.1'
    )

    token = "12345"
    start_time = datetime.strptime("00:00:00", "%H:%M:%S")
    types = ["TEMPERATURE", "HUMIDITY_SOIL", "HUMIDITY_AIR", "WATER_LEVEL"]
    data_to_insert = []

    for minute in range(24 * 60):
        current_time = (start_time + timedelta(minutes=minute)).time()
        for sensor_type in types:
            value = random.randint(0, 100)
            data_to_insert.append((sensor_type, current_time, token, value))

    await conn.executemany("""
        INSERT INTO sensor_data (type, time, token, value)
        VALUES ($1, $2, $3, $4)
    """, data_to_insert)

    print(f"Добавлено {len(data_to_insert)} записей.")
    await conn.close()

# Запускаем
asyncio.run(fill_sensor_data())
