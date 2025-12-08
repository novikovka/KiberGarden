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
from database import get_token_by_telegram_id

router = Router()

class Gen(StatesGroup):
    wait = State()

@router.message(F.text.lower() == "задать свой вопрос нейросети")
async def handle_request_word(message: Message, state: FSMContext):
    await message.answer("Напишите ваш запрос...")
    await state.set_state(Gen.wait)

@router.message(Gen.wait)
async def generating(message: Message, state: FSMContext):
    await message.answer("Ваш запрос обрабатывается...")
    response = await ai_generate(message.text)
    await message.answer(response)
    await state.clear()


async def get_last_24_hours_summary(pool, token):
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

def create_initial_plant_prompt(plant_name: str) -> str:
    return f"""
Ты — агроном со специализацией на выращивании растений в теплицах.

Дай подробные рекомендации по выращиванию растения: {plant_name}.

Обязательно укажи:
1. Основные принципы ухода.
2. Сколько раз в день нужно поливать и в какие часы.
3. Какую температуру нужно поддерживать.
4. Какую влажность почвы нужно поддерживать.
5. Какую влажность воздуха нужно поддерживать.
6. Любые дополнительные советы по условиям в теплице.

Формат ответа: структурированный, понятный, в виде списка.
"""



async def process_recommendation(user_id: int):
    token = await get_token_by_telegram_id(user_id)

    sensor_summary = await get_last_24_hours_summary(db.pool, token)
    plant_name = await get_user_plant_name(user_id)

    prompt = create_plant_care_prompt(sensor_summary, plant_name)
    print(prompt)

    response = await ai_generate(prompt)


    # Сохраняем в БД
    now = datetime.now()

    async with db.pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT token FROM recommendations WHERE token = $1",
            token
        )

        if existing:
            await conn.execute("""
                UPDATE recommendations
                SET text = $1, date = $2
                WHERE token = $3
            """, response, now, token)
        else:
            await conn.execute("""
                INSERT INTO recommendations (token, text, date)
                VALUES ($1, $2, $3)
            """, token, response, now)

    return response



@router.message(F.text.lower() == "запросить у нейросети новые рекомендации")
async def analyze_data(message: Message):
    #token = get_token_by_telegram_id(message.from_user.id)
    token = await get_token_by_telegram_id(message.from_user.id)

    sensor_summary = await get_last_24_hours_summary(db.pool, token)

    user_id = message.from_user.id
    plant_name = await get_user_plant_name(user_id)

    prompt = create_plant_care_prompt(sensor_summary, plant_name)

    await message.answer("Формирую промт для нейросети...")
    print(prompt)  # отладка

    # Генерация нейросетевого ответа
    response = await ai_generate(prompt)

    # Отправляем пользователю
    await message.answer(response)

    # -----------------------------
    # 🔥 Сохранение или обновление в БД
    # -----------------------------
    now = datetime.now()

    async with db.pool.acquire() as conn:

        # Проверяем, есть ли запись с таким token
        existing = await conn.fetchrow(
            "SELECT token FROM recommendations WHERE token = $1",
            token
        )

        if existing:
            # Обновляем text и date
            await conn.execute(
                """
                UPDATE recommendations
                SET text = $1, date = $2
                WHERE token = $3
                """,
                response, now, token
            )
        else:
            # Создаём запись
            await conn.execute(
                """
                INSERT INTO recommendations (token, text, date)
                VALUES ($1, $2, $3)
                """,
                token, response, now
            )

    print("Recommendation saved/updated for token:", token)


