from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup #для состояний
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

#импортируем все по отношению к main
import keyboards as kb
#from database import pool
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
    time_obj = previous_minute.time()  # <-- вот ключевое изменение

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

'''
@router.message(Command("state"))
async def cmd_state(message: Message):
    user_id = message.from_user.id

    # Получаем токен пользователя (если у тебя есть такая функция)
    token = await get_token_by_telegram_id(user_id)

    # SQL-запрос: берём по одному последнему значению каждого типа
    query = """
        SELECT DISTINCT ON (type) type, value, time
        FROM sensor_data
        WHERE token = $1
        ORDER BY type, time DESC
    """

    async with database.pool.acquire() as conn:
        rows = await conn.fetch(query, token)

    # Создаём словарь из результатов
    data = {row["type"]: row["value"] for row in rows}

    # Подставляем значения (если чего-то нет, ставим "-")
    text_state = (
        "Текущие показания датчиков:\n\n"
        f"🌡 Температура: {data.get('TEMPERATURE', '-')}°C\n"
        f"💧 Влажность воздуха: {data.get('HUMIDITY_AIR', '-')}%\n"
        f"🌱 Влажность почвы: {data.get('HUMIDITY_SOIL', '-')}%\n"
        f"🚰 Уровень воды: {data.get('WATER_LEVEL', '-')}%\n"
    )

    await message.answer(text_state)
    
'''

