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

class AddNewNotification(StatesGroup):
    notification_type = State()
    notification_value = State()

class RemoveNotification(StatesGroup):
    not_remove_type = State()
    not_remove_value = State()

### Переход из основного меню в раздел уведомлений
@router.message(Command('notifications'))
async def cmd_notifications(message: Message):
    user_id = message.from_user.id
    token = await get_token_by_telegram_id(user_id)

    # Запрос в базу данных
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

    # Формируем текст
    type_map = {
        "TEMPERATURE": "🌡 Температура воздуха",
        "HUMIDITY_AIR": "💧 Влажность воздуха",
        "HUMIDITY_SOIL": "🌱 Влажность почвы",
        "WATER_LEVEL": "🚰 Уровень воды",
    }

    text_lines = ["Триггеры уведомлений:\n"]
    for row in rows:
        sensor_name = type_map.get(row["type"], row["type"])
        value = row["value"]

        # Форматирование единиц измерения
        if row["type"] == "TEMPERATURE":
            text_lines.append(f"{sensor_name}: {value}°C")
        elif row["type"] in ("HUM_AIR", "HUM_SOIL", "WATER_LEVEL"):
            text_lines.append(f"{sensor_name}: {value}%")
        else:
            text_lines.append(f"{sensor_name}: {value}")

    # Отправляем пользователю красиво оформленный текст
    await message.answer("\n".join(text_lines), reply_markup=kb.set_notifications)


### Добавление нового триггера уведомлений

@router.callback_query(F.data == "add_trigger")
async def add_new_notification(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddNewNotification.notification_type)
    await callback.message.answer(
        "Выберите тип нового триггера",
        reply_markup=kb.new_notification_type
    )
    await callback.answer()

@router.callback_query(AddNewNotification.notification_type)
async def add_notification_type(callback: CallbackQuery, state: FSMContext):
    chosen_type = callback.data

    # ✅ Обработка кнопки "Отменить"
    if chosen_type == "cancel":
        await callback.message.answer("Добавление нового триггера уведомлений отменено ✅")
        await state.clear()  # очищаем состояние
        await callback.answer()
        return

    # Сохраняем выбранный тип
    await state.update_data(notification_type=chosen_type)

    # ✅ Обрабатываем выбранные типы триггеров
    if chosen_type == "temperature":
        await callback.message.answer("Введите значение температуры воздуха при котором Вы хотите получать уведомление:")
        await state.set_state(AddNewNotification.notification_value)

    elif chosen_type == "humidity_air":
        await callback.message.answer("Введите значение влажности воздуха при котором Вы хотите получать уведомление:")
        await state.set_state(AddNewNotification.notification_value)

    elif chosen_type == "humidity_soil":
        await callback.message.answer("Введите значение влажности почвы при котором Вы хотите получать уведомление:")
        await state.set_state(AddNewNotification.notification_value)

    else:
        await callback.message.answer("Неизвестная команда, попробуйте снова.")

    await callback.answer()


@router.message(AddNewNotification.notification_value)
async def add_notification_value(message: Message, state: FSMContext):
    new_value = message.text.strip()
    await state.update_data(notification_value= int(new_value))

    # Получаем все данные
    data = await state.get_data()
    user_id = message.from_user.id
    token = await get_token_by_telegram_id(user_id)
    notification_type = data["notification_type"].upper()

    async with database.pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO notifications (type, token, value) VALUES ($1, $2, $3)",
            notification_type, token, data["notification_value"]
        )

    await message.answer(
        f"✅ Новый триггер уведомления добавлен:\n"
        f"Тип: {data['notification_type']}\n"
        f"Значение: {data['notification_value']}"
    )

    # Очистить состояние
    await state.clear()


### Удаление триггера уведомлений
@router.callback_query(F.data == "remove_trigger")
async def remove_notification(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RemoveNotification.not_remove_type)
    await callback.message.answer(
        "Выберите тип триггера для удаления:",
        reply_markup=kb.remove_notifications
    )
    await callback.answer()

@router.callback_query(RemoveNotification.not_remove_type)
async def remove_notification_type(callback: CallbackQuery, state: FSMContext):
    chosen_type = callback.data

    # ✅ Обработка кнопки "Отменить"
    if chosen_type == "cancel":
        await callback.message.answer("Удаление триггера уведомлений отменено ✅")
        await state.clear()  # очищаем состояние
        await callback.answer()
        return

    # Сохраняем выбранный тип
    await state.update_data(not_remove_type=chosen_type)

    # ✅ Обрабатываем выбранные типы триггеров
    if chosen_type == "temperature":
        await callback.message.answer("Введите значение триггера температуры который Вы хотите удалить:")
        await state.set_state(RemoveNotification.not_remove_value)

    elif chosen_type == "humidity_air":
        await callback.message.answer("Введите значение триггера влажности воздуха который Вы хотите удалить:")
        await state.set_state(RemoveNotification.not_remove_value)

    elif chosen_type == "humidity_soil":
        await callback.message.answer("Введите значение триггера влажности почвы который Вы хотите удалить:")
        await state.set_state(RemoveNotification.not_remove_value)

    else:
        await callback.message.answer("Неизвестная команда, попробуйте снова.")

    await callback.answer()

@router.message(RemoveNotification.not_remove_value)
async def remove_notification_value(message: Message, state: FSMContext):
    new_value = message.text.strip()
    await state.update_data(not_remove_value= int(new_value))

    # Получаем все данные
    data = await state.get_data()
    user_id = message.from_user.id
    token = await get_token_by_telegram_id(user_id)
    notification_type = data["not_remove_type"].upper()

    async with database.pool.acquire() as conn:
        await conn.execute(
            "DELETE FROM notifications WHERE type = $1 AND token = $2 AND value = $3",
            notification_type, token, data["not_remove_value"]
        )

    await message.answer(
        f"✅ Триггер уведомления {data['not_remove_type']}, \n"
        f"значение: {data['not_remove_value']} - удален!\n"
    )

    # Очистить состояние
    await state.clear()
