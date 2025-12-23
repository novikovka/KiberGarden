from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

class ConnectionGuardMiddleware(BaseMiddleware):

    # Команды, которые не блокируются при аварии
    ALLOWED_COMMANDS = {"/start", "/help", "/register"}

    def __init__(self, pool):
        self.pool = pool

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ):

        if not isinstance(event, Message):
            return await handler(event, data)

        text = event.text or ""
        if any(text.startswith(cmd) for cmd in self.ALLOWED_COMMANDS):
            return await handler(event, data)

        telegram_id = event.from_user.id

        # проверяем connection в БД
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT connection
                FROM users
                WHERE telegram_id = $1
                """,
                telegram_id
            )

        # если пользователь не найден — не блокируем
        if row is None:
            return await handler(event, data)

        # если аварийный режим — блокируем
        if row["connection"] is False:
            await event.answer(
                "❌ Связь с устройством потеряна.\n"
                "Проверьте подключение устройства к сети."
            )
            return

        # всё хорошо — аварии нет, продолжаем обработку
        return await handler(event, data)
