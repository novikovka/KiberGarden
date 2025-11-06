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

class AddNewAction(StatesGroup):
    action_type = State()
    action_time = State()
    action_status = State()
    #token = State()

text_settings = (
    "Настройки системы:\n\n"
    f"💡 Включить освещение: 12:00\n"
    f"💧 Включить полив: 12:30\n"
    f"🌬 Включить проветривание: 16:00\n"
)

@router.message(Command('schedule'))
async def cmd_schedule(message: Message):
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

    await callback.message.answer(
        f"Вы выбрали: {action_type} ({'включить' if action_status == True else 'выключить'})\n"
        "Введите время выполнения (например, 12:00):"
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

    # Пример вывода
    await message.answer(
        f"✅ Новое действие добавлено:\n"
        f"Тип: {data['action_type']}\n"
        f"Статус: {data['action_status']}\n"
        f"Время: {data['action_time']}"
    )

    # Очистить состояние
    await state.clear()
