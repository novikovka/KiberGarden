from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='каталог')],
                                     [KeyboardButton(text='вторая')],
                                     [KeyboardButton(text='третья'), KeyboardButton(text='четвертая')]],
                           resize_keyboard=True, input_field_placeholder='Выберите пункт меню')

'''
catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='футболки', callback_data='T-shirt')],
                                                [InlineKeyboardButton(text='кроссовки', callback_data='sneakers')],
                                                [InlineKeyboardButton(text='кепки', callback_data='cap')]])
'''

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True)]], resize_keyboard=True)

#управление поливом
watering_control = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='включить', callback_data='on_watering'),
                                                          InlineKeyboardButton(text='выключить', callback_data='off_watering')]])

light_control = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='включить', callback_data='on_light'),
                                                InlineKeyboardButton(text='выключить', callback_data='off_light')]])

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
                                                [InlineKeyboardButton(text='выключение проветривания', callback_data='add_vent_off')]])

