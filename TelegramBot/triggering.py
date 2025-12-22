from database import pool, get_telegram_id_by_token


# Человеко-читаемые шаблоны уведомлений
SENSOR_MESSAGES = {
    "HUMIDITY_AIR": "⚠️ Значение влажности воздуха достигло {value} %!",
    "TEMPERATURE": "⚠️ Температура достигла {value} °C!",
    "HUMIDITY_SOIL": "⚠️ Влажность почвы достигла {value} %!",
    "WATER_LEVEL": "⚠️ Уровень воды в резервуаре  {value} %!",
}


def format_sensor_alert(sensor_type: str, value):
    """
    Формирует текст уведомления для пользователя
    """
    template = SENSOR_MESSAGES.get(
        sensor_type,
        "⚠️ Критическое значение датчика ({type}): {value}"
    )
    return template.format(type=sensor_type, value=value)


async def check_notifications(bot, pool):
    """
    Проверяет критические показания датчиков в текущую минуту
    и отправляет уведомления пользователям.
    """

    async with pool.acquire() as conn:
        query = """
        SELECT s.type, s.token, s.value, s.time
        FROM sensor_data s
        JOIN notifications n
          ON s.type = n.type
         AND s.token = n.token
         AND s.value = n.value
        WHERE (CURRENT_DATE + s.time) = date_trunc('minute', NOW());
        """

        rows = await conn.fetch(query)

    for row in rows:
        sensor_type = row["type"]
        token = row["token"]
        value = row["value"]
        time_ = row["time"]

        telegram_id = await get_telegram_id_by_token(token)

        if telegram_id:
            text = format_sensor_alert(sensor_type, value)

            await bot.send_message(
                chat_id=telegram_id,
                text=text
            )

        print(
            f"[ALERT] Совпадение: "
            f"type={sensor_type}, value={value}, token={token}, time={time_}"
        )

    if rows:
        print(f"Найдено {len(rows)} критических записей.")


### Аварийное состояние

from aiogram import Bot

async def check_user_connections(bot: Bot, pool):
    async with pool.acquire() as conn:

        # 1️⃣ Потеря связи → уведомляем ОДИН раз
        lost_rows = await conn.fetch(
            """
            SELECT telegram_id
            FROM users
            WHERE connection = false
              AND connection_notified = false
            """
        )

        for row in lost_rows:
            telegram_id = row["telegram_id"]

            try:
                await bot.send_message(
                    telegram_id,
                    "❌ Связь с устройством потеряна! Теплица переведена в автономное состояние."
                )

                await conn.execute(
                    """
                    UPDATE users
                    SET connection_notified = true
                    WHERE telegram_id = $1
                    """,
                    telegram_id
                )

            except Exception as e:
                print(f"Ошибка отправки (lost) {telegram_id}: {e}")

        # 2️⃣ Связь восстановлена → уведомляем
        restored_rows = await conn.fetch(
            """
            SELECT telegram_id
            FROM users
            WHERE connection = true
              AND connection_notified = true
            """
        )

        for row in restored_rows:
            telegram_id = row["telegram_id"]

            try:
                await bot.send_message(
                    telegram_id,
                    "✅ Связь с устройством восстановлена!"
                )

                await conn.execute(
                    """
                    UPDATE users
                    SET connection_notified = false
                    WHERE telegram_id = $1
                    """,
                    telegram_id
                )

            except Exception as e:
                print(f"Ошибка отправки (restored) {telegram_id}: {e}")



'''
from database import pool, get_telegram_id_by_token


async def check_notifications(bot, pool):
    """
    Проверяет критические показания датчиков в текущую минуту
    и отправляет уведомления пользователям.
    """

    async with pool.acquire() as conn:
        query = """
        SELECT s.type, s.token, s.value, s.time
        FROM sensor_data s
        JOIN notifications n
          ON s.type = n.type
         AND s.token = n.token
         AND s.value = n.value
        WHERE (CURRENT_DATE + s.time) = date_trunc('minute', NOW());
        """

        rows = await conn.fetch(query)

    # обработка совпадений
    for row in rows:
        type_ = row["type"]
        token = row["token"]
        value = row["value"]
        time_ = row["time"]

        telegram_id = await get_telegram_id_by_token(token)

        if telegram_id:
            await bot.send_message(
                chat_id=telegram_id,
                text=(
                    "⚠️ Критическое показание датчика!\n"
                    f"Тип: {type_}\n"
                    f"Значение: {value}\n"
                    f"Время: {time_}"
                )
            )

        print(f"[ALERT] Совпадение: {type_}, value={value}, token={token}, time={time_}")

    if rows:
        print(f"Найдено {len(rows)} критических записей.")
'''