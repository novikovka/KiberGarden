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
