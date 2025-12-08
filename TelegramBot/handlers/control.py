from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup #для состояний
from aiogram.fsm.context import FSMContext
from datetime import datetime
import aiohttp

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



async def send_to_server(token: str, system_type: str, status: bool):
    """
    HTTP-запрос к серверу теплицы.
    Отправляет JSON: {token, type, status}
    """
    url = "http://5.189.97.105:8080/api/createActions"

    payload = {
        "token": token,
        "type": system_type,
        "status": status
    }
    print(payload)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    return f"Ошибка сервера: {resp.status}"
                return await resp.text()

        except Exception as e:
            return f"Не удалось отправить команду на сервер: {e}"


# ------------------ ОБРАБОТЧИК КНОПОК ------------------

@router.callback_query(F.data.regexp(r"^(watering|light|emergency)_(on|off)$"))
async def toggle_device(callback: CallbackQuery):
    user_id = callback.from_user.id
    token = await get_token_by_telegram_id(user_id)
    await callback.answer()  # быстрый ответ

    # Извлекаем данные: watering_on → ["watering", "on"]
    device_type_raw, action = callback.data.split("_")

    device_type = device_type_raw.upper()   # WATERING / LIGHT / EMERGENCY
    is_on = action == "on"                  # bool

    # Обновляем состояние в БД
    async with database.pool.acquire() as conn:
        await conn.execute("""
            UPDATE current_state
            SET status = $1
            WHERE token = $2 AND type = $3
        """, is_on, token, device_type)

    # Отправляем команду на сервер
    server_response = await send_to_server(token, device_type, is_on)

    # Формируем ответ пользователю
    device_name = device_names.get(device_type, device_type)

    status_text = "Включено" if is_on else "Выключено"
    message_text = f"{device_name}: {status_text}"

    keyboard = keyboards[device_type](is_on)

    # Короткий popup над кнопкой
    await callback.answer(f"{device_name} {status_text.lower()} ✅")

    # Обновляем сообщение
    await callback.message.edit_text(message_text, reply_markup=keyboard)

    # -------- 4) Если сервер вернул ошибку — уведомляем пользователя --------

    if server_response.startswith("Ошибка") or "не удалось" in server_response.lower():
        await callback.message.answer(f"⚠️ {server_response}")


'''
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

'''
