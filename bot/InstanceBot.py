import os

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties

bot = Bot(
    token=os.getenv("BOT_API_TOKEN"),
    default=DefaultBotProperties(parse_mode="HTML"),
)
dp = Dispatcher()
router = Router()
dp.include_router(router)
