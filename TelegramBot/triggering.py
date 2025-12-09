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
