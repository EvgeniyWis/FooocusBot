from aiogram import Dispatcher, Router, Bot
import os
from aiogram.client.default import DefaultBotProperties

bot = Bot(token=os.getenv("BOT_API_TOKEN"), default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
router = Router()
dp.include_router(router)