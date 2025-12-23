from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import keyboards as kb
import database
from database import get_token_by_telegram_id
from ai.handlers import process_recommendation

# Импортируем функцию из graph.py
from .graphs import send_graphs

router = Router()

@router.message(Command("analytics"))
async def get_recommendation(message: Message):
    # Сначала отправляем графики
    await message.answer("📈 Графики суточных показаний датчиков:")
    await send_graphs(message)

    user_id = message.from_user.id
    token = await get_token_by_telegram_id(user_id)

    async with database.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT text FROM recommendations WHERE token = $1",
            token
        )

    if row is None:
        await message.answer("Пока нет рекомендаций для вашего устройства 🌱")
    else:
        await message.answer(
            row["text"],
            reply_markup=kb.analytics_keyboard  # добавляем клавиатуру
        )


@router.callback_query(F.text == "запросить у нейросети новые рекомендации")
async def analyze_data_callback(callback: CallbackQuery):
    await callback.message.answer("Формирую промт для нейросети...")

    response = await process_recommendation(callback.from_user.id)

    await callback.message.answer(response)
    await callback.answer()
