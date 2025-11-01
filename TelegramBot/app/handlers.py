from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup #для состояний
from aiogram.fsm.context import FSMContext
from datetime import datetime

#импортируем все по отношению к main
import app.keyboards as kb
#from database import pool
import database

router = Router()

class Register(StatesGroup):
    name = State()
    #ip_address = State()
    token = State()
    plat_name = State()
    telegram_id = State()


class AddNewAction(StatesGroup):
    action_type = State()
    action_time = State()
    action_status = State()
    #token = State()

text_state = (
            "Текущие показания датчиков:\n\n"
            f"🌡 Температура: 35°C\n"
            f"💧 Влажность воздуха: 80%\n"
            f"🌱 Влажность почвы: 91%\n"
            f"🚰 Уровень воды: 23 %\n"
        )

text_settings = (
    "Настройки системы:\n\n"
    f"💡 Включить освещение: 12:00\n"
    f"💧 Включить полив: 12:30\n"
    f"🌬 Включить проветривание: 16:00\n"
)

notifications_triggers = (
    "Триггеры уведомлений:\n\n"
    f"💧 Влажность воздуха: 80%\n"
    f"🌡 Температура воздуха: 40°C\n"
    f"🌱 Влажность почвы: 70%\n"
)

@router.callback_query(F.data == "add_settings")
async def add_settings_type(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddNewAction.action_type)
    await callback.message.answer(
        "Выберите тип нового действия:",
        reply_markup=kb.new_action_type
    )
    await callback.answer()


@router.callback_query(F.data.startswith("add_"), AddNewAction.action_type)
async def add_settings_select(callback: CallbackQuery, state: FSMContext):
    data = callback.data

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
        f"Вы выбрали: {action_type} ({'включить' if action_status == 'True' else 'выключить'})\n"
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

    time_text = data["action_time"]
    action_time = datetime.strptime(time_text, "%H:%M").time()
    action_type = data["action_type"].upper()


    async with database.pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO actions (status, time, type, telegram_id) VALUES ($1, $2, $3, $4)",
            data['action_status'], action_time, action_type, user_id  # <-- не оборачиваем user_id в str()
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


################ получение данных из базы

@router.message(lambda m: m.text and m.text.lower().strip() == "строка")
async def get_all_users(message: Message):
    if database.pool is None:
        await message.answer("❌ База данных не инициализирована.")
        return

    async with database.pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM users')

        if not rows:
            await message.answer("Таблица пустая.")
            return

        response = "\n".join(
            f"telegram_id: {r['telegram_id']}, "
            f"name: {r['name']}, "
            f"plant_name: {r['plant_name']}, "
            f"token: {r['token']}"
            for r in rows
        )

        await message.answer(response)


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


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hello!', reply_markup=kb.main)
    await message.reply('How are you?')

@router.message(Command('state'))
async def cmd_state(message: Message):
    await message.answer(text_state)

@router.message(Command('control'))
async def control(message: Message):
    await message.answer('Полив: ', reply_markup=kb.watering_control)
    await message.answer('Освещение: ', reply_markup=kb.light_control)
    await message.answer('Проветривание: ', reply_markup=kb.ventilation_control)

@router.message(Command('schedule'))
async def cmd_schedule(message: Message):
    await message.answer(text_settings, reply_markup=kb.set_settings)

@router.message(Command('notifications'))
async def cmd_notifications(message: Message):
    await message.answer(notifications_triggers, reply_markup=kb.set_notifications)





