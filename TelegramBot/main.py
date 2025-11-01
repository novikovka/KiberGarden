import asyncio
import asyncpg
from aiogram import Bot, Dispatcher
from app.handlers import router
from database import init_db, close_db

bot = Bot(token='8246553812:AAGEjCIdml2DsBfA3e4UeyHzjWb4SUwDv6w')
dp = Dispatcher()

async def main():
    # Подключаем роутеры до старта polling
    dp.include_router(router)

    # Инициализируем базу данных
    await init_db()

    try:
        # Запускаем бота
        await dp.start_polling(bot)
    finally:
        # Корректно закрываем соединения
        await close_db()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")



