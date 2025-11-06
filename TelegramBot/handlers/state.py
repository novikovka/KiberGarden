from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup #для состояний
from aiogram.fsm.context import FSMContext
from datetime import datetime

#импортируем все по отношению к main
import keyboards as kb
#from database import pool
import database
from database import get_token_by_telegram_id
from database import get_current_status


router = Router()

'''
text_state = (
            "Текущие показания датчиков:\n\n"
            f"🌡 Температура: 35°C\n"
            f"💧 Влажность воздуха: 80%\n"
            f"🌱 Влажность почвы: 91%\n"
            f"🚰 Уровень воды: 23 %\n"
        )

@router.message(Command('state'))
async def cmd_state(message: Message):
    await message.answer(text_state)

'''
@router.message(Command('state'))
async def cmd_state(message: Message):
    user_id = message.from_user.id
    token = await get_token_by_telegram_id(user_id)

    sensors = {
        "temperature": ("🌡 Температура", "°C"),
        "humidity_air": ("💧 Влажность воздуха", "%"),
        "humidity_soil": ("🌱 Влажность почвы", "%"),
        "water_level": ("🚰 Уровень воды", "%")
    }

    result_text = "Текущие показания датчиков:\n\n"

    async with database.pool.acquire() as conn:
        for sensor_type, (label, unit) in sensors.items():
            row = await conn.fetchrow(
                """
                SELECT value 
                FROM sensor_data
                WHERE type = $1 AND token = $2
                ORDER BY time DESC
                LIMIT 1
                """,
                sensor_type.upper(), token
            )

            if row:
                result_text += f"{label}: {row['value']}{unit}\n"
            else:
                result_text += f"{label}: ❌ нет данных\n"

    await message.answer(result_text)

