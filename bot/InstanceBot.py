import os

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import find_dotenv, load_dotenv

from bot.factory.redis_factory import create_redis_client

load_dotenv(find_dotenv())

from dotenv import load_dotenv
from logger import logger

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'FocuuusBot', '.env')
logger.info(f"Путь к .env файлу: {env_path}")
logger.info(f"Файл .env существует: {os.path.exists(env_path)}")

if 'BOT_API_TOKEN' in os.environ:
    del os.environ['BOT_API_TOKEN']

load_dotenv(env_path, override=True)

# Создаём бота
bot = Bot(
    token=os.getenv("BOT_API_TOKEN"),
    default=DefaultBotProperties(parse_mode="HTML"),
)

redis_client = create_redis_client()
storage = RedisStorage(redis_client)

dp = Dispatcher(storage=storage)
router = Router()

# Увеличиваем таймаут для запросов к Telegram API
bot.session = AiohttpSession(timeout=60)


dp.include_router(router)
