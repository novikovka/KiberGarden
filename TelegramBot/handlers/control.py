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

device_names = {
    "WATERING": "Полив",
    "LIGHT": "Освещение",
    "EMERGENCY": "Проветривание"
}

keyboards = {
    "WATERING": kb.watering_control,
    "LIGHT": kb.light_control,
    "EMERGENCY": kb.emergency_control
}

# Описание систем: тип, название и функция для клавиатуры
systems = [
    ("WATERING", "Полив", kb.watering_control),
    ("LIGHT", "Освещение", kb.light_control),
    ("EMERGENCY", "Проветривание", kb.emergency_control),
]

@router.message(Command("control"))
async def control(message: Message):
    user_id = message.from_user.id
    token = await get_token_by_telegram_id(user_id)

    # Проходим по всем системам
    for system_type, system_name, keyboard_func in systems:
        status = await get_current_status(token, system_type)

        if status is None:
            await message.answer(
                f"⚠️ Не найдено состояние для системы: {system_name}. Возможно, устройство ещё не подключено.")
            continue

        # Формируем текст статуса
        text = f"{system_name}: {'Включено' if status else 'Выключено'}"

        # Отправляем сообщение с соответствующей клавиатурой
        await message.answer(text, reply_markup=keyboard_func(status))


@router.callback_query(F.data.regexp(r"^(watering|light|emergency)_(on|off)$"))
async def toggle_device(callback: CallbackQuery):
    user_id = callback.from_user.id
    token = await get_token_by_telegram_id(user_id)

    # Извлекаем тип устройства и действие
    match = callback.data.split("_")
    device_type, action = match[0].upper(), match[1]  # например -> WATERING, ON
    is_on = action == "on"

    # Обновляем статус в БД
    async with database.pool.acquire() as conn:
        await conn.execute("""
            UPDATE current_state
            SET status = $1
            WHERE token = $2 AND type = $3
        """, is_on, token, device_type)

    # Формируем текст ответа и клавиатуру
    device_name = device_names.get(device_type, device_type)
    message_text = f"{device_name}: {'Включено' if is_on else 'Отключено'}"
    keyboard = keyboards[device_type](is_on)

    # Отправляем ответ
    await callback.answer(f"{device_name} {'включено' if is_on else 'отключено'} ✅")

    # Обновляем сообщение
    await callback.message.edit_text(message_text, reply_markup=keyboard)


