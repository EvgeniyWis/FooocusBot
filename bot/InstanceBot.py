import os

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
from logger import logger

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "FocuuusBot", ".env")
logger.info(f"Путь к .env файлу: {env_path}")
logger.info(f"Файл .env существует: {os.path.exists(env_path)}")

if "BOT_API_TOKEN" in os.environ:
    del os.environ["BOT_API_TOKEN"]
    del os.environ["KLING_API_KEY"]

load_dotenv(env_path, override=True)

# Выводим KLING_API_KEY для проверки
kling_api_key = os.environ.get("KLING_API_KEY")
logger.info(f"KLING_API_KEY из .env: {kling_api_key}")

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
