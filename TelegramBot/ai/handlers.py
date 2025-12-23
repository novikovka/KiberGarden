from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.text_decorations import html_decoration as hd
from ai.generate import ai_generate
import database as db
from database import get_user_plant_name, get_token_by_telegram_id
import json
from datetime import datetime, timedelta

router = Router()

class Gen(StatesGroup):
    wait = State()

# Экранирует HTML-символы и безопасно отправляет сообщение
async def safe_answer(message: Message, text: str):
    await message.answer(
        hd.quote(text),
        parse_mode="HTML"
    )

@router.message(F.text.lower() == "задать свой вопрос нейросети")
async def handle_request_word(message: Message, state: FSMContext):
    await message.answer("Напишите ваш запрос...")
    await state.set_state(Gen.wait)

@router.message(Gen.wait)
async def generating(message: Message, state: FSMContext):
    await message.answer("Ваш запрос обрабатывается...")
    response = await ai_generate(message.text)
    await safe_answer(message, response)
    await state.clear()

# Получение данных за последние 24 часа
async def get_last_24_hours_summary(pool, token):
    """
    Получает средние почасовые данные за последние 24 часа
    и формирует словарь (для последующей передачи в JSON).
    """
    async with pool.acquire() as conn:
        now = datetime.now()
        result_data = []

        hours_list = [
            (now - timedelta(hours=i))
            .time()
            .replace(minute=0, second=0, microsecond=0)
            for i in range(23, -1, -1)
        ]

        for hour_time in hours_list:
            query = """
                SELECT type, AVG(value) as avg_value
                FROM sensor_data
                WHERE token = $1 
                  AND EXTRACT(HOUR FROM time) = $2
                GROUP BY type
            """
            rows = await conn.fetch(query, token, hour_time.hour)

            hour_data = {
                "temperature": None,
                "humidity_air": None,
                "humidity_soil": None
            }

            for row in rows:
                if row["type"] == "TEMPERATURE":
                    hour_data["temperature"] = float(row["avg_value"])
                elif row["type"] == "HUMIDITY_AIR":
                    hour_data["humidity_air"] = float(row["avg_value"])
                elif row["type"] == "HUMIDITY_SOIL":
                    hour_data["humidity_soil"] = float(row["avg_value"])

            result_data.append({
                "time": hour_time.strftime("%H:%M:%S"),
                "data": hour_data
            })

        return {
            "token": token,
            "period": "last_24_hours",
            "data": result_data
        }

def create_plant_care_prompt(sensor_json: dict, plant_name: str) -> str:
    return (
        f"У тебя есть данные с датчиков растения '{plant_name}' "
        "за последние 24 часа в формате JSON:\n\n"
        f"{json.dumps(sensor_json, ensure_ascii=False, indent=2)}\n\n"
        "Поля:\n"
        "- time — время усреднённых показаний\n"
        "- data.temperature — температура воздуха (°C)\n"
        "- data.humidity_air — влажность воздуха (%)\n"
        "- data.humidity_soil — влажность почвы (%)\n\n"
        "Проанализируй данные и дай рекомендации:\n"
        "1. Полив\n"
        "2. Проветривание\n"
        "3. Температура и освещение\n\n"
        "Если всё в норме — напиши: 'Никаких действий не требуется'."
    )


def create_initial_plant_prompt(plant_name: str) -> str:
    return f"""
Ты — агроном со специализацией на выращивании растений в теплицах.

Дай подробные рекомендации по выращиванию растения: {plant_name}.

Обязательно укажи:
1. Основные принципы ухода
2. Полив (частота и время)
3. Температуру
4. Влажность почвы
5. Влажность воздуха
6. Дополнительные советы

Формат: структурированный список.
"""

async def process_recommendation(user_id: int):
    token = await get_token_by_telegram_id(user_id)
    plant_name = await get_user_plant_name(user_id)

    sensor_summary = await get_last_24_hours_summary(db.pool, token)
    prompt = create_plant_care_prompt(sensor_summary, plant_name)

    response = await ai_generate(prompt)
    now = datetime.now()

    async with db.pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT token FROM recommendations WHERE token = $1",
            token
        )

        if existing:
            await conn.execute(
                """
                UPDATE recommendations
                SET text = $1, date = $2
                WHERE token = $3
                """,
                response, now, token
            )
        else:
            await conn.execute(
                """
                INSERT INTO recommendations (token, text, date)
                VALUES ($1, $2, $3)
                """,
                token, response, now
            )

    return response


@router.message(F.text == "Запросить у нейросети новые рекомендации")
async def analyze_data(message: Message):
    user_id = message.from_user.id

    token = await get_token_by_telegram_id(user_id)
    plant_name = await get_user_plant_name(user_id)

    sensor_summary = await get_last_24_hours_summary(db.pool, token)
    prompt = create_plant_care_prompt(sensor_summary, plant_name)

    await message.answer("Анализирую данные и формирую рекомендации...")
    response = await ai_generate(prompt)

    await safe_answer(message, response)

    now = datetime.now()
    async with db.pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT token FROM recommendations WHERE token = $1",
            token
        )

        if existing:
            await conn.execute(
                """
                UPDATE recommendations
                SET text = $1, date = $2
                WHERE token = $3
                """,
                response, now, token
            )
        else:
            await conn.execute(
                """
                INSERT INTO recommendations (token, text, date)
                VALUES ($1, $2, $3)
                """,
                token, response, now
            )

    print("Recommendation saved/updated for token:", token)

