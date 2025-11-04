from aiogram import F, Router
from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup #для состояний
from aiogram.fsm.context import FSMContext
from datetime import datetime

#импортируем все по отношению к main
import app.keyboards as kb
#from database import pool
import database
from database import get_token_by_telegram_id


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

class AddNewNotification(StatesGroup):
    notification_type = State()
    notification_value = State()

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
### добавление нового запланированного действия
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
            "INSERT INTO actions (status, time, token, type, telegram_id) VALUES ($1, $2, $3, $4, $5)",
            data["action_status"], action_time, token, action_type, user_id
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
    # Сохраняем то, что выбрал пользователь
    chosen_type = callback.data
    await state.update_data(notification_type=chosen_type)

    # Отвечаем пользователю в зависимости от выбора
    if chosen_type == "temperature":
        await callback.message.answer("Введите значение температуры воздуха при котором Вы хотите получать уводомление:")
        await state.set_state(AddNewNotification.notification_value)

    elif chosen_type == "hum_air":
        await callback.message.answer("Введите значение влажности воздуха при котором Вы хотите получать уводомление:")
        await state.set_state(AddNewNotification.notification_value)
        # await state.set_state(AddNewNotification.sensor_choice)

    elif chosen_type == "hum_soil":
        await callback.message.answer("Введите значение влажности почвы при котором Вы хотите получать уводомление:")
        await state.set_state(AddNewNotification.notification_value)
        # await state.set_state(AddNewNotification.weather_input)

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
            "INSERT INTO notifications (type, token, value, telegram_id) VALUES ($1, $2, $3, $4)",
            notification_type, token, data["notification_value"], user_id
        )

    await message.answer(
        f"✅ Новый триггер уведомления добавлен:\n"
        f"Тип: {data['notification_type']}\n"
        f"Значение: {data['notification_value']}"
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
    await message.answer('Hello!')
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





