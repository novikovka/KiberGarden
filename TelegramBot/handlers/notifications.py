from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import database
from database import get_token_by_telegram_id
import keyboards as kb

router = Router()

###  Конфигурация типов уведомлений
NOTIFICATION_TYPES = {
    "temperature": {
        "db": "TEMPERATURE",
        "title": "Температура воздуха",
        "emoji": "🌡",
        "unit": "°C",
        "add_prompt": "Введите температуру, при которой отправлять уведомление:",
        "del_prompt": "Введите значение триггера температуры, который нужно удалить:",
    },
    "humidity_air": {
        "db": "HUMIDITY_AIR",
        "title": "Влажность воздуха",
        "emoji": "💧",
        "unit": "%",
        "add_prompt": "Введите влажность воздуха для уведомления:",
        "del_prompt": "Введите значение триггера влажности воздуха для удаления:",
    },
    "humidity_soil": {
        "db": "HUMIDITY_SOIL",
        "title": "Влажность почвы",
        "emoji": "🌱",
        "unit": "%",
        "add_prompt": "Введите влажность почвы для уведомления:",
        "del_prompt": "Введите значение триггера влажности почвы для удаления:",
    },
    "water_level": {
        "db": "WATER_LEVEL",
        "title": "Уровень воды",
        "emoji": "🚰",
        "unit": "%",
        "add_prompt": "Введите уровень воды для уведомления:",
        "del_prompt": "Введите значение триггера уровня воды для удаления:",
    },
}

class AddNotificationState(StatesGroup):
    type = State()
    value = State()

class RemoveNotificationState(StatesGroup):
    type = State()
    value = State()

###  Команда /notifications
@router.message(Command("notifications"))
async def cmd_notifications(message: Message):
    user_id = message.from_user.id
    token = await get_token_by_telegram_id(user_id)

    async with database.pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT type, value
            FROM notifications
            WHERE token = $1
            ORDER BY type
        """, token)

    if not rows:
        await message.answer("🔔 Уведомления пока не настроены.", reply_markup=kb.set_notifications)
        return

    text_lines = ["Триггеры уведомлений:\n"]

    for row in rows:
        info = next((v for v in NOTIFICATION_TYPES.values() if v["db"] == row["type"]), None)
        if info:
            text_lines.append(f"{info['emoji']} {info['title']}: {row['value']}{info['unit']}")
        else:
            text_lines.append(f"{row['type']}: {row['value']}")

    await message.answer("\n".join(text_lines), reply_markup=kb.set_notifications)


###  Добавление триггера
@router.callback_query(F.data == "add_trigger")
async def add_trigger(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddNotificationState.type)
    await callback.message.answer("Выберите тип нового триггера:", reply_markup=kb.new_notification_type)
    await callback.answer()


@router.callback_query(AddNotificationState.type)
async def add_trigger_type(callback: CallbackQuery, state: FSMContext):
    type_key = callback.data

    if type_key == "cancel":
        await callback.message.answer("Добавление триггера отменено.")
        await state.clear()
        return

    info = NOTIFICATION_TYPES.get(type_key)
    if not info:
        await callback.message.answer("Неизвестный тип триггера.")
        return

    await state.update_data(type=type_key)
    await state.set_state(AddNotificationState.value)

    await callback.message.answer(info["add_prompt"])
    await callback.answer()

@router.message(AddNotificationState.value)
async def add_trigger_value(message: Message, state: FSMContext):
    value_text = message.text.strip()

    if not value_text.isdigit():
        await message.answer("Введите число, пожалуйста.")
        return

    value = int(value_text)
    data = await state.get_data()

    type_key = data["type"]
    info = NOTIFICATION_TYPES[type_key]

    token = await get_token_by_telegram_id(message.from_user.id)

    async with database.pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO notifications (type, token, value) VALUES ($1, $2, $3)",
            info["db"], token, value
        )

    await message.answer(f"✅ Триггер добавлен!\n{info['title']}: {value}{info['unit']}")
    await state.clear()

###  Удаление триггера
@router.callback_query(F.data == "remove_trigger")
async def remove_trigger(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RemoveNotificationState.type)
    await callback.message.answer("Выберите тип триггера для удаления:", reply_markup=kb.remove_notifications)
    await callback.answer()

@router.callback_query(RemoveNotificationState.type)
async def remove_trigger_type(callback: CallbackQuery, state: FSMContext):
    type_key = callback.data

    if type_key == "cancel":
        await callback.message.answer("Удаление триггера отменено.")
        await state.clear()
        return

    info = NOTIFICATION_TYPES.get(type_key)
    if not info:
        await callback.message.answer("Неизвестный тип триггера.")
        return

    await state.update_data(type=type_key)
    await state.set_state(RemoveNotificationState.value)

    await callback.message.answer(info["del_prompt"])
    await callback.answer()

@router.message(RemoveNotificationState.value)
async def remove_trigger_value(message: Message, state: FSMContext):
    value_text = message.text.strip()

    if not value_text.isdigit():
        await message.answer("Введите число, пожалуйста.")
        return

    value = int(value_text)
    data = await state.get_data()

    type_key = data["type"]
    info = NOTIFICATION_TYPES[type_key]

    token = await get_token_by_telegram_id(message.from_user.id)

    async with database.pool.acquire() as conn:
        await conn.execute(
            "DELETE FROM notifications WHERE type = $1 AND token = $2 AND value = $3",
            info["db"], token, value
        )

    await message.answer(f"✅ Триггер удалён!\n{info['title']}: {value}{info['unit']}")
    await state.clear()
