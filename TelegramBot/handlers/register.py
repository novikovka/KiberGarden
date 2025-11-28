from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup #для состояний
from aiogram.fsm.context import FSMContext
from datetime import datetime
from ai.generate import ai_generate

#импортируем все по отношению к main
import keyboards as kb
#from database import pool
import database
from database import get_token_by_telegram_id
from database import get_current_status

router = Router()

class Register(StatesGroup):
    name = State()
    #ip_address = State()
    token = State()
    plat_name = State()
    telegram_id = State()


# Команда для начала регистрации
@router.message(F.text.lower() == "/register")
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Здравствуйте! Введите ваше имя: ")
    await state.set_state(Register.name)

@router.message(Register.name)
async def get_ip(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите токен вашей теплицы:")
    await state.set_state(Register.token)

@router.message(Register.token)
async def get_ip(message: Message, state: FSMContext):
    await state.update_data(token=message.text)
    await message.answer("Какое растение вы хотите выращивать?")
    await state.set_state(Register.plat_name)

'''
@router.message(Register.plat_name)
async def get_token(message: Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data["name"]
    token = user_data["token"]
    plant_name = message.text
    user_id = message.from_user.id

    async with database.pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO users (telegram_id, name, plant_name, token) VALUES ($1, $2, $3, $4)",
            user_id, name, plant_name, token
        )

    await message.answer("✅ Регистрация завершена! Данные сохранены в базу.")
    await state.clear()
'''

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


@router.message(Register.plat_name)
async def finish_registration(message: Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data["name"]
    token = user_data["token"]
    plant_name = message.text
    user_id = message.from_user.id

    # 1. Сохраняем пользователя в БД
    async with database.pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users (telegram_id, name, plant_name, token)
            VALUES ($1, $2, $3, $4)
            """,
            user_id, name, plant_name, token
        )

    # 2. Создаём промпт для нейросети
    prompt = create_initial_plant_prompt(plant_name)

    # 3. Вызываем нейросеть
    try:
        await message.answer("Запрашиваю рекомендации у нейросети... Подождите пару секунд ⏳")
        ai_response = await ai_generate(prompt)
    except Exception as e:
        await message.answer("⚠ Ошибка при запросе к нейросети. Попробуйте позже.")
        print(e)
        await state.clear()
        return

    # 4. Отправляем рекомендации пользователю
    await message.answer(
        f"🌱 Отлично, вы выбрали растение: <b>{plant_name}</b>\n\n"
        f"Вот рекомендации по его выращиванию:\n\n"
        f"{ai_response}",
        parse_mode="HTML"
    )

    await message.answer("Регистрация завершена! 🎉")

    # Сохраняем рекомендации в БД
    now = datetime.now()

    async with database.pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT token FROM recommendations WHERE token = $1",
            token
        )

        if existing:
            await conn.execute("""
                    UPDATE recommendations
                    SET text = $1, date = $2
                    WHERE token = $3
                """, ai_response, now, token)
        else:
            await conn.execute("""
                    INSERT INTO recommendations (token, text, date)
                    VALUES ($1, $2, $3)
                """, token, ai_response, now)

    await state.clear()
