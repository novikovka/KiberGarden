from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup #для состояний
from aiogram.fsm.context import FSMContext

#импортируем все по отношению к main
import app.keyboards as kb

router = Router()

class Register(StatesGroup):
    name = State()
    token = State()
    plant_name = State()
    phone = State()

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




