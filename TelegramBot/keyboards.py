from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True)]], resize_keyboard=True)

ventilation_control = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='включить', callback_data='on_ventilation'),
                                                InlineKeyboardButton(text='выключить', callback_data='off_ventilation')]])

set_settings = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='добавить действие', callback_data='add_settings')],
                                                [InlineKeyboardButton(text='удалить действие', callback_data='remove_settings')]])

set_notifications = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='добавить триггер', callback_data='add_trigger')],
                                                [InlineKeyboardButton(text='удалить триггер', callback_data='remove_trigger')]])

remove_notifications = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Температура воздуха', callback_data='temperature')],
                                                [InlineKeyboardButton(text='Влажность воздуха', callback_data='humidity_air')],
                                                [InlineKeyboardButton(text='Влажность почвы', callback_data='humidity_soil')],
                                                [InlineKeyboardButton(text='уровень воды в резервуаре', callback_data='water_level')],
                                                [InlineKeyboardButton(text='🚫 отменить', callback_data='cancel')]])

remove_action = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='включение полива', callback_data='rm_watering_on')],
                                                [InlineKeyboardButton(text='включение освещения', callback_data='rm_light_on')],
                                                [InlineKeyboardButton(text='выключение освещения', callback_data='rm_light_off')],
                                                [InlineKeyboardButton(text='включение проветривания', callback_data='rm_emergency_on')],
                                                [InlineKeyboardButton(text='выключение проветривания', callback_data='rm_emergency_off')],
                                                [InlineKeyboardButton(text='🚫 отменить', callback_data='cancel')]])

new_action_type = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='включение полива', callback_data='add_watering_on')],
                                                [InlineKeyboardButton(text='включение освещения', callback_data='add_light_on')],
                                                [InlineKeyboardButton(text='выключение освещения', callback_data='add_light_off')],
                                                [InlineKeyboardButton(text='включение проветривания', callback_data='add_emergency_on')],
                                                [InlineKeyboardButton(text='выключение проветривания', callback_data='add_emergency_off')],
                                                [InlineKeyboardButton(text='🚫 отменить', callback_data='cancel')]])

new_notification_type = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='температура воздуха', callback_data='temperature')],
                                                [InlineKeyboardButton(text='влажность воздуха', callback_data='humidity_air')],
                                                [InlineKeyboardButton(text='влажность почвы', callback_data='humidity_soil')],
                                                [InlineKeyboardButton(text='уровень воды в резервуаре', callback_data='water_level')],
                                                [InlineKeyboardButton(text='🚫 отменить', callback_data='cancel')]])


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

analytics_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Запросить у нейросети новые рекомендации')]],
    resize_keyboard=True,
    one_time_keyboard=False
)

def watering_control(is_on: bool) -> InlineKeyboardMarkup:
    if is_on:
        # Полив включён → показываем кнопку выключения
        button = InlineKeyboardButton(
            text="🚫 Выключить полив",
            callback_data="watering_off"
        )
    else:
        # Полив выключен → показываем кнопку включения
        button = InlineKeyboardButton(
            text="💧 Включить полив",
            callback_data="watering_on"
        )

    return InlineKeyboardMarkup(inline_keyboard=[[button]])

def light_control(is_on: bool) -> InlineKeyboardMarkup:
    if is_on:
        button = InlineKeyboardButton(
            text="🚫 Выключить освещение",
            callback_data="light_off"
        )
    else:
        button = InlineKeyboardButton(
            text="💡 Включить освещение",
            callback_data="light_on"
        )

    return InlineKeyboardMarkup(inline_keyboard=[[button]])

def emergency_control(is_on: bool) -> InlineKeyboardMarkup:
    if is_on:
        button = InlineKeyboardButton(
            text="🚫 Выключить проветривание",
            callback_data="emergency_off"
        )
    else:
        button = InlineKeyboardButton(
            text="🌬 Включить проветривание",
            callback_data="emergency_on"
        )

    return InlineKeyboardMarkup(inline_keyboard=[[button]])


