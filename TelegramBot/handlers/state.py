from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from datetime import datetime, timedelta

import database
from database import get_token_by_telegram_id
from database import get_current_status

router = Router()

@router.message(Command("state"))
async def cmd_state(message: Message):
    user_id = message.from_user.id
    token = await get_token_by_telegram_id(user_id)

    # Определяем предыдущую минуту
    now = datetime.now()
    previous_minute = (now - timedelta(minutes=1)).replace(second=0, microsecond=0)
    time_obj = previous_minute.time()

    # Запрашиваем данные из БД
    query = """
        SELECT type, value
        FROM sensor_data
        WHERE token = $1 AND time = $2
    """

    async with database.pool.acquire() as conn:
        rows = await conn.fetch(query, token, time_obj)

    # Преобразуем результат в словарь
    data = {row["type"]: row["value"] for row in rows}

    # Формируем сообщение
    text_state = (
        f"🌡 Температура: {data.get('TEMPERATURE', '-')}°C\n"
        f"💧 Влажность воздуха: {data.get('HUMIDITY_AIR', '-')}%\n"
        f"🌱 Влажность почвы: {data.get('HUMIDITY_SOIL', '-')}%\n"
        f"🚰 Уровень воды: {data.get('WATER_LEVEL', '-')}%\n"
    )

    await message.answer(text_state)

