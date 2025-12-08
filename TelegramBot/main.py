import asyncio
import asyncpg
from aiogram import Bot, Dispatcher

import database
from app.handlers import router
from database import init_db, close_db
from handlers.init import routers
from ai.handlers import process_recommendation  # импорт функции

from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = Bot(token='8246553812:AAGEjCIdml2DsBfA3e4UeyHzjWb4SUwDv6w')
dp = Dispatcher()


async def run_cron_job():
    """Выполняем process_recommendation для всех пользователей."""
    async with database.pool.acquire() as conn:
        # Замените 'telegram_id' на реальное имя колонки с ID пользователей
        rows = await conn.fetch("SELECT telegram_id FROM users")
        for row in rows:
            user_id = row["telegram_id"]
            await process_recommendation(user_id)

    print("Cron job finished")


def schedule_cron_job():
    """Запуск cron job через APScheduler."""
    scheduler = AsyncIOScheduler()
    # Запуск каждый день в 12:00
    scheduler.add_job(run_cron_job, 'cron', hour=17, minute=31)
    scheduler.start()


async def main():
    # Подключаем роутеры
    for r in routers:
        dp.include_router(r)

    # Инициализируем базу данных
    await init_db()

    # --------------------------
    # 🔥 Планировщик APScheduler
    # --------------------------
    schedule_cron_job()

    try:
        # Запускаем бота
        await dp.start_polling(bot)
    finally:
        await close_db()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
