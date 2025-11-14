import asyncio
from aiogram import Bot, Dispatcher
#from config import TG_TOKEN

from app.handlers import router

TG_TOKEN='8078703880:AAFCvkv7Gh3XjnAZZK742oVdHzUfVet-fJ8'

async def main():
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot) #ищем обновления

if __name__ == '__main__':
    asyncio.run(main())