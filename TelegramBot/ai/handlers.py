from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from ai.generate import ai_generate
import database as db
import json
from datetime import datetime, timedelta

import database
from database import get_user_plant_name

router = Router()

class Gen(StatesGroup):
    wait = State()

@router.message(F.text.lower() == "запрос")
async def handle_request_word(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать, напишите ваш запрос")
    await state.set_state(Gen.wait)

@router.message(Gen.wait)
async def generating(message: Message, state: FSMContext):
    await message.answer("Ваш запрос обрабатывается...")
    response = await ai_generate(message.text)
    await message.answer(response)
    await state.clear()


async def get_last_24_hours_summary(pool, token: str):
    """
    Получает средние почасовые данные за последние 24 часа
    и формирует JSON для нейросети.
    """
    async with pool.acquire() as conn:
        now = datetime.now()
        result_data = []

        # Создаём список часов за последние 24 часа
        hours_list = [(now - timedelta(hours=i)).time().replace(minute=0, second=0, microsecond=0)
                      for i in range(23, -1, -1)]

        for hour_time in hours_list:
            # Берём все записи за этот час
            query = """
                SELECT type, AVG(value) as avg_value
                FROM sensor_data
                WHERE token = $1 
                  AND EXTRACT(HOUR FROM time) = $2
                GROUP BY type
            """
            rows = await conn.fetch(query, token, hour_time.hour)

            # Инициализируем словарь для этого часа
            hour_data = {
                "temperature": None,
                "humidity_air": None,
                "humidity_soil": None
            }

            for row in rows:
                if row['type'] == 'TEMPERATURE':
                    hour_data['temperature'] = float(row['avg_value'])
                elif row['type'] == 'HUMIDITY_AIR':
                    hour_data['humidity_air'] = float(row['avg_value'])
                elif row['type'] == 'HUMIDITY_SOIL':
                    hour_data['humidity_soil'] = float(row['avg_value'])

            result_data.append({
                "time": hour_time.strftime("%H:%M:%S"),
                "data": hour_data
            })

        final_result = {
            "token": token,
            "period": "last_24_hours",
            "data": result_data
        }

        return final_result  # возвращаем словарь, чтобы потом можно было сразу в JSON


def create_plant_care_prompt(sensor_json: dict, plant_name: str) -> str:
    """
    Формирует промт для нейросети на основе данных датчиков и названия растения.
    """
    prompt = (
        f"У тебя есть данные с датчиков комнатного растения '{plant_name}' "
        "за последние 24 часа в формате JSON:\n\n"
        f"{json.dumps(sensor_json, ensure_ascii=False, indent=2)}\n\n"
        "Поля:\n"
        "- time — время усреднённых показаний\n"
        "- data.temperature — температура воздуха в градусах\n"
        "- data.humidity_air — влажность воздуха в процентах\n"
        "- data.humidity_soil — влажность почвы в процентах\n\n"
        "Проанализируй данные и дай рекомендации по уходу за этим растением:\n"
        "- Нужно ли поливать, и если да — сколько и когда\n"
        "- Нужно ли проветривать\n"
        "- Нужно ли менять температуру или освещение\n\n"
        "Ответь в формате:\n"
        "1. Рекомендация по поливу\n"
        "2. Рекомендация по проветриванию\n"
        "3. Рекомендация по температуре/освещению\n\n"
        "Если данные в норме, укажи 'Никаких действий не требуется'."
    )
    return prompt


@router.message(F.text.lower() == "анализ")
async def analyze_data(message: Message):
    token = "12345"  # можно получить из профиля пользователя
    sensor_summary = await get_last_24_hours_summary(db.pool, token)

    user_id = message.from_user.id
    plant_name = await get_user_plant_name(user_id)
    prompt = create_plant_care_prompt(sensor_summary, plant_name)

    await message.answer("Формирую промт для нейросети...")
    print(prompt)  # для отладки

    response = await ai_generate(prompt)
    await message.answer(response)

