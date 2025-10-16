from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup #для состояний
from aiogram.fsm.context import FSMContext

#импортируем все по отношению к main
import app.keyboards as kb
#from database import pool
import database

router = Router()

class Register(StatesGroup):
    waiting_for_ip = State()
    waiting_for_token = State()

class AddNewAction(StatesGroup):
    action_type = State()
    action_time = State()

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
################ получение данных из базы

@router.message(lambda m: m.text and m.text.lower().strip() == "строка")
async def get_all_users(message: Message):
    if database.pool is None:
        await message.answer("❌ База данных не инициализирована.")
        return

    async with database.pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM users_tbl')

        if not rows:
            await message.answer("Таблица пустая.")
            return

        response = "\n".join(
            f"id_tg_user: {r['id_tg_user']}, "
            f"ip_greenhouse: {r['ip_greenhouse']}, "
            f"id_token_greenhouse: {r['id_token_greenhouse']}"
            for r in rows
        )

        await message.answer(response)

################ регистрация и запись данных в бд


# --- Команда для начала регистрации ---
@router.message(F.text.lower() == "/register")
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Введите IP адрес вашей теплицы:")
    await state.set_state(Register.waiting_for_ip)


# --- Получаем IP и переходим к следующему шагу ---
@router.message(Register.waiting_for_ip)
async def get_ip(message: Message, state: FSMContext):
    await state.update_data(ip_greenhouse=message.text)
    await message.answer("Введите токен вашей теплицы:")
    await state.set_state(Register.waiting_for_token)


# --- Получаем токен и записываем всё в базу ---
@router.message(Register.waiting_for_token)
async def get_token(message: Message, state: FSMContext):
    user_data = await state.get_data()
    ip = user_data["ip_greenhouse"]
    token = message.text
    user_id = message.from_user.id  # <-- это уже int

    async with database.pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO users_tbl (id_tg_user, ip_greenhouse, id_token_greenhouse) VALUES ($1, $2, $3)",
            user_id, ip, token  # <-- не оборачиваем user_id в str()
        )

    await message.answer("✅ Регистрация завершена! Данные сохранены в базу.")
    await state.clear()


#################

@router.message(CommandStart()) #говорим что обрабатываем сообщения
async def cmd_start(message: Message):
    await message.answer('Hello!', reply_markup=kb.main)
    await message.reply('How are you?')

@router.message(Command('state')) #говорим что обрабатываем сообщения
async def cmd_state(message: Message):
    await message.answer(text_state)

@router.message(Command('control'))
async def control(message: Message):
    await message.answer('Полив: ', reply_markup=kb.watering_control)
    await message.answer('Освещение: ', reply_markup=kb.light_control)
    await message.answer('Проветривание: ', reply_markup=kb.ventilation_control)

@router.message(Command('schedule')) #говорим что обрабатываем сообщения
async def cmd_schedule(message: Message):
    await message.answer(text_settings, reply_markup=kb.set_settings)

@router.message(Command('notifications')) #говорим что обрабатываем сообщения
async def cmd_notifications(message: Message):
    await message.answer(notifications_triggers, reply_markup=kb.set_notifications)

'''
@router.message(F.text == 'у меня все хорошо') #говорим что обрабатываем сообщения
async def nice(message: Message):
    await message.reply('Я очень рад')

@router.message(F.text == 'каталог') #говорим что обрабатываем сообщения
async def catalog(message: Message):
    await message.answer('выберите категорию товара: ', reply_markup=kb.catalog)

@router.callback_query(F.data == 'T-shirt')
async def t_shirt(callback: CallbackQuery):
    await callback.message.answer('Вы выбрали категорю футболок.')
'''
'''

@router.callback_query(F.data == 'add_settings')
async def add_settings_type(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddNewAction.action_type)  # устанавливаем состояние
    await callback.message.answer('Выберите тип нового действия', reply_markup=kb.new_action_type)

@router.callback_query(F.data == "add_watering_on")
async def add_settings_time(callback: CallbackQuery, state: FSMContext):
    await state.update_data(action_type="add_watering_on")  # лучше не использовать "type" как имя
    await state.set_state(AddNewAction.action_time)  # установить состояние
    await callback.message.answer("Введите время включения полива:")
    await callback.answer()  # обязательно ответить на callback, чтобы убрать «часики» в Telegram

@router.message(AddNewAction.action_time)
async def end_added_action(message: Message, state: FSMContext):
    await state.update_data(action_time = message.text)
    data = await state.get_data()
    await message.answer(f'Запланированно новое действие: '
                         f'Время: {data["action_time"]} \n '
                         f'Тип: {data["action_type"]} \n ')
    await state.clear() #очистили состояние пользователя
    
'''

@router.callback_query(F.data == 'add_settings')
async def add_settings_type(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddNewAction.action_type)
    await callback.message.answer(
        'Выберите тип нового действия:',
        reply_markup=kb.new_action_type
    )
    await callback.answer()


# --- Один обработчик для всех типов действий ---
@router.callback_query(F.data.in_({
    "add_watering_on",
    "add_light_on",
    "add_light_off",
    "add_vent_on",
    "add_vent_off"
}))
async def add_settings_time(callback: CallbackQuery, state: FSMContext):
    action_type = callback.data
    await state.update_data(action_type=action_type)
    await state.set_state(AddNewAction.action_time)

    messages = {
        "add_watering_on": "Введите время включения полива:",
        "add_light_on": "Введите время включения света:",
        "add_light_off": "Введите время выключения света:",
        "add_vent_on": "Введите время включения вентиляции:",
        "add_vent_off": "Введите время выключения вентиляции:"
    }

    await callback.message.answer(messages.get(action_type, "Введите время действия:"))
    await callback.answer()


@router.message(AddNewAction.action_time)
async def end_added_action(message: Message, state: FSMContext):
    await state.update_data(action_time=message.text)
    data = await state.get_data()

    action_names = {
        "add_watering_on": "Включение полива",
        "add_light_on": "Включение света",
        "add_light_off": "Выключение света",
        "add_vent_on": "Включение проветривания",
        "add_vent_off": "Выключение проветривания"
    }

    action_text = action_names.get(data["action_type"], data["action_type"])
    action_time = data["action_time"]

    await message.answer(
        f"✅ Запланировано новое действие:\n"
        f"👉 {action_text} в {action_time}"
    )

    await state.clear()


'''

# мы не можем словить имя потому что оно у всех разное,
# поэтому присваиваем пользователю состояние пока он вводит имя и потом будем отлавливать это состояние
@router.message(Command('register'))
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name) #устанавливаем состояние
    await message.answer('Введите ваше имя')

@router.message(Register.name) #ловим состояние "name"
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.token) #устанавливаем состояние
    await message.answer('Введите токен вашей теплицы')

@router.message(Register.token)
async def register_token(message: Message, state: FSMContext):
    await state.update_data(token=message.text)
    await state.set_state(Register.plant_name) #устанавливаем состояние
    await message.answer('Введите название растения которое вы хотите выращивать')

@router.message(Register.plant_name)
async def register_plant_name(message: Message, state: FSMContext):
    await state.update_data(plant_name=message.text)
    await state.set_state(Register.phone) #устанавливаем состояние
    await message.answer('Отправьте ваш номер телефона', reply_markup=kb.get_number)

@router.message(Register.phone)
async def register_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    await message.answer(f'Ваше имя: {data["name"]} \n '
                         f'Ваш токен: {data["token"]} \n '
                         f'Ваше растение: {data["plant_name"]} \n '
                         f'Ваш номер: {data["phone"]} \n')
    await state.clear() #очистили состояние пользователя

'''


