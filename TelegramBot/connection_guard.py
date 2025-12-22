from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable


class ConnectionGuardMiddleware(BaseMiddleware):

    # 👇 команды, которые НЕ блокируются даже при аварии
    ALLOWED_COMMANDS = {"/start", "/help", "/register"}

    def __init__(self, pool):
        self.pool = pool

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ):

        # 1️⃣ обрабатываем только сообщения
        if not isinstance(event, Message):
            return await handler(event, data)

        # 2️⃣ разрешённые команды — сразу пропускаем
        text = event.text or ""
        if any(text.startswith(cmd) for cmd in self.ALLOWED_COMMANDS):
            return await handler(event, data)

        telegram_id = event.from_user.id

        # 3️⃣ читаем connection из БД
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT connection
                FROM users
                WHERE telegram_id = $1
                """,
                telegram_id
            )

        # 4️⃣ пользователь не найден — не блокируем
        if row is None:
            return await handler(event, data)

        # 5️⃣ ❌ аварийный режим — блокируем
        if row["connection"] is False:
            await event.answer(
                "❌ Связь с устройством потеряна.\n"
                "Проверьте подключение устройства к сети."
            )
            return  # ⛔ дальше handler НЕ вызывается

        # 6️⃣ ✅ всё хорошо — продолжаем обработку
        return await handler(event, data)
