import os

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

# Создаём бота
bot = Bot(
    token=os.getenv("BOT_API_TOKEN"),
    default=DefaultBotProperties(parse_mode="HTML"),
)

dp = Dispatcher()
router = Router()

# Увеличиваем таймаут для запросов к Telegram API
bot.session = AiohttpSession(timeout=60)


dp.include_router(router)
