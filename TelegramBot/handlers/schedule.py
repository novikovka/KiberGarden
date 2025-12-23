from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup #для состояний
from aiogram.fsm.context import FSMContext
from datetime import datetime

#импортируем все по отношению к main
import keyboards as kb
import database
from database import get_token_by_telegram_id

router = Router()

class AddNewAction(StatesGroup):
    action_type = State()
    action_time = State()
    action_status = State()

class RemoveAction(StatesGroup):
    action_type = State()
    action_time = State()
    action_status = State()

@router.message(Command('schedule'))
async def cmd_schedule(message: Message):
    user_id = message.from_user.id
    token = await get_token_by_telegram_id(user_id)

    async with database.pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT type, status, time
            FROM actions
            WHERE token = $1
            ORDER BY time
        """, token)

    if not rows:
        await message.answer(
            "⚙️ Расписание пока не задано. Вы можете добавить время включения в настройках.",
            reply_markup=kb.set_settings
        )
        return

    icons = {
        "WATERING": "💧 Полив",
        "LIGHT": "💡 Освещение",
        "EMERGENCY": "🌬 Проветривание"
    }

    # Формируем текст расписания
    text_lines = ["Настройки системы:\n"]

    for row in rows:
        action_time = row["time"].strftime("%H:%M") if row["time"] else "—"
        device_name = icons.get(row["type"], row["type"].title())

        if row["status"]:
            line = f"{device_name}: включение в {action_time}"
        else:
            line = f"{device_name}: выключение в {action_time}"

        text_lines.append(line)

    text_settings = "\n".join(text_lines)

    await message.answer(text_settings, reply_markup=kb.set_settings)


### добавление нового запланированного действия
@router.callback_query(F.data == "add_settings")
async def add_settings_type(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddNewAction.action_type)
    await callback.message.answer(
        "Выберите тип нового действия:",
        reply_markup=kb.new_action_type
    )
    await callback.answer()


@router.callback_query((F.data.startswith("add_") | (F.data == "cancel")),AddNewAction.action_type)
async def add_settings_select(callback: CallbackQuery, state: FSMContext):
    data = callback.data

    if data == "cancel":
        await callback.message.answer("Добавление нового действия отменено ✅")
        await state.clear()  # очищаем состояние
        await callback.answer()
        return

    # формат: add_<тип>_<статус>
    _, action_type, action_status = data.split("_")
    print(action_type)
    action_status = True if action_status == "on" else False

    # Сохраняем данные в состояние
    await state.update_data(
        action_type=action_type,
        action_status=action_status
    )

    # Сопоставление технического типа действия с нормальным названием
    pretty_action = {
        "emergency": "проветривания",
        "watering": "полива",
        "light": "освещения"
    }.get(action_type, action_type)

    # Формируем текст: включение/выключение + действие
    action_phrase = f"{'включение' if action_status else 'выключение'} {pretty_action}"

    await callback.message.answer(
        f"Вы выбрали: {action_phrase}\n"
        "Введите время выполнения действия, которое вы хотите добавить (например, 12:00):"
    )

    # Переход к следующему состоянию
    await state.set_state(AddNewAction.action_time)
    await callback.answer()


@router.message(AddNewAction.action_time)
async def add_settings_time(message: Message, state: FSMContext):
    time_text = message.text.strip()

    import re
    if not re.match(r"^\d{1,2}:\d{2}$", time_text):
        await message.answer("Введите время в формате HH:MM, например 09:30")
        return

    # Сохраняем время
    await state.update_data(action_time=time_text)

    # Получаем все данные
    data = await state.get_data()
    user_id = message.from_user.id

    #time_text = data["action_time"]
    action_time = datetime.strptime(data["action_time"], "%H:%M").time()
    action_type = data["action_type"].upper()
    #action_status = data["action_status"]
    token = await get_token_by_telegram_id(user_id)

    async with database.pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO actions (status, time, token, type) VALUES ($1, $2, $3, $4)",
            data["action_status"], action_time, token, action_type
        )

    pretty_action = {
        "watering": "полива",
        "light": "освещения",
        "emergency": "проветривания"
    }.get(data['action_type'], data['action_type'])

    # Формируем текст: включение / выключение
    status_text = "Включение" if data['action_status'] else "Выключение"

    # Итоговое сообщение
    await message.answer(
        f"✅ Новое действие добавлено:\n"
        f"{status_text} {pretty_action} в {data['action_time']}."
    )

    # Очистить состояние
    await state.clear()

### удаление действия
@router.callback_query(F.data == "remove_settings")
async def remove_settings_type(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RemoveAction.action_type)
    await callback.message.answer(
        "Выберите тип действия для удаления:",
        reply_markup=kb.remove_action
    )
    await callback.answer()

@router.callback_query((F.data.startswith("rm_") | (F.data == "cancel")),RemoveAction.action_type)
async def rm_settings_select(callback: CallbackQuery, state: FSMContext):
    data = callback.data

    if data == "cancel":
        await callback.message.answer("Удаление действия отменено ✅")
        await state.clear()  # очищаем состояние
        await callback.answer()
        return

    # формат: add_<тип>_<статус>
    _, action_type, action_status = data.split("_")
    print(action_type)
    action_status = True if action_status == "on" else False

    # Сохраняем данные в состояние
    await state.update_data(
        action_type=action_type,
        action_status=action_status
    )

    # Сопоставление технического типа действия с нормальным названием
    pretty_action = {
        "emergency": "проветривания",
        "watering": "полива",
        "light": "освещения"
    }.get(action_type, action_type)

    # Формируем текст: включение/выключение + действие
    action_phrase = f"{'включение' if action_status else 'выключение'} {pretty_action}"

    await callback.message.answer(
        f"Вы выбрали: {action_phrase}\n"
        "Введите время выполнения действия, которое вы хотите удалить(например, 12:00):"
    )

    # Переход к следующему состоянию
    await state.set_state(RemoveAction.action_time)
    await callback.answer()

@router.message(RemoveAction.action_time)
async def rm_settings_time(message: Message, state: FSMContext):
    time_text = message.text.strip()

    import re
    if not re.match(r"^\d{1,2}:\d{2}$", time_text):
        await message.answer("Введите время в формате HH:MM, например 09:30")
        return

    # Сохраняем время
    await state.update_data(action_time=time_text)

    # Получаем все данные
    data = await state.get_data()
    user_id = message.from_user.id

    action_time = datetime.strptime(data["action_time"], "%H:%M").time()
    action_type = data["action_type"].upper()
    #action_status = data["action_status"]
    token = await get_token_by_telegram_id(user_id)
    print(data["action_status"], action_time, token, action_type)

    async with database.pool.acquire() as conn:
        await conn.execute(
            "DELETE FROM actions WHERE status = $1 AND time = $2 AND token = $3 AND type = $4",
            data["action_status"], action_time, token, action_type
        )

    # action_type может приходить в формате "WATERING", "LIGHT", "VENTILATION"
    action_type_lower = action_type.lower()

    pretty_action = {
        "watering": "полива",
        "lighting": "освещения",
        "light": "освещения",  # на случай LIGHT
        "ventilation": "проветривания",
        "emergency": "проветривания"
    }.get(action_type_lower, action_type_lower)

    # Включение / выключение
    status_text = "включение" if data["action_status"] else "выключение"
    time_str = action_time.strftime("%H:%M")

    await message.answer(
        f"🗑 Действие удалено: {status_text} {pretty_action} в {time_str}."
    )

    # Очистить состояние
    await state.clear()

