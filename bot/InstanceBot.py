import os

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import find_dotenv, load_dotenv

from utils.factory.redis_factory import create_redis_client

load_dotenv(find_dotenv())

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
