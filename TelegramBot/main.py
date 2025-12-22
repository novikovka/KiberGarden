import asyncio
from aiogram import Bot, Dispatcher

import database
from database import init_db, close_db
from handlers.init import routers
from ai.handlers import process_recommendation

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from triggering import check_notifications
from triggering import check_user_connections
from connection_guard import ConnectionGuardMiddleware


bot = Bot(token='8246553812:AAGEjCIdml2DsBfA3e4UeyHzjWb4SUwDv6w')
dp = Dispatcher()

scheduler = AsyncIOScheduler()   # один общий scheduler


async def run_cron_job(pool):
    """Запускается каждый день — вызывает рекомендации для всех пользователей."""
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT telegram_id FROM users")
        for row in rows:
            user_id = row["telegram_id"]
            await process_recommendation(user_id)

    print("Cron job finished")


def schedule_jobs(pool):
    """Регистрация всех cron-задач"""

    # ежедневная задача
    scheduler.add_job(
        run_cron_job,
        'cron',
        hour=17,
        minute=31,
        args=[pool]
    )

    # проверка критических показаний каждую минуту
    scheduler.add_job(
        check_notifications,
        "interval",
        minutes=1,
        args=[bot, pool]      # <— передаём pool
    )

    # проверка соединения с устройством
    scheduler.add_job(
        check_user_connections,
        "interval",
        minutes=1,
        args=[bot, pool]
    )

    scheduler.start()


async def main():
    # Подключение роутеров
    for r in routers:
        dp.include_router(r)

    await init_db()

    dp.message.middleware(
        ConnectionGuardMiddleware(database.pool)
    )

    # Запуск фоновых задач — после init_db()
    schedule_jobs(database.pool)

    try:
        await dp.start_polling(bot)
    finally:
        await close_db()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
