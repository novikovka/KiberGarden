from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True)]], resize_keyboard=True)

ventilation_control = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='включить', callback_data='on_ventilation'),
                                                InlineKeyboardButton(text='выключить', callback_data='off_ventilation')]])

set_settings = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='добавить действие', callback_data='add_settings')],
                                                [InlineKeyboardButton(text='удалить действие', callback_data='remove_settings')]])

set_notifications = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='добавить триггер', callback_data='add_trigger')],
                                                [InlineKeyboardButton(text='удалить триггер', callback_data='remove_trigger')]])

new_action_type = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='включение полива', callback_data='add_watering_on')],
                                                [InlineKeyboardButton(text='включение освещения', callback_data='add_light_on')],
                                                [InlineKeyboardButton(text='выключение освещения', callback_data='add_light_off')],
                                                [InlineKeyboardButton(text='включение проветривания', callback_data='add_vent_on')],
                                                [InlineKeyboardButton(text='выключение проветривания', callback_data='add_vent_off')],
                                                [InlineKeyboardButton(text='🚫 отменить', callback_data='cancel')]])

new_notification_type = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='температура воздуха', callback_data='temperature')],
                                                [InlineKeyboardButton(text='влажность воздуха', callback_data='hum_air')],
                                                [InlineKeyboardButton(text='влажность почвы', callback_data='hum_soil')],
                                                [InlineKeyboardButton(text='🚫 отменить', callback_data='cancel')]])


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


