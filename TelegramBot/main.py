import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from app.handlers import router

bot = Bot(token='8246553812:AAGEjCIdml2DsBfA3e4UeyHzjWb4SUwDv6w')
dp = Dispatcher()

async def main():
    dp.include_router(router) #добавили один роутер (они могут быть отдельные для пользователя и для сервера)
    await dp.start_polling(bot) #обращаемся к телеграмму и спрашиваем не пришло ли какое то обновление

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("бот выключен")





