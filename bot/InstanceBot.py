import os
from datetime import timedelta

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import find_dotenv, load_dotenv

from bot.factory.redis_factory import create_redis_client

load_dotenv(find_dotenv())

# Создаём бота
bot = Bot(
    token=os.getenv("BOT_API_TOKEN"),
    default=DefaultBotProperties(parse_mode="HTML"),
)

redis_client = create_redis_client()

storage = RedisStorage(
    redis=redis_client,
    state_ttl=timedelta(days=15),
    data_ttl=timedelta(days=3),
)

dp = Dispatcher(storage=storage)
router = Router()

# Увеличиваем таймаут для запросов к Telegram API
bot.session = AiohttpSession(timeout=60)


dp.include_router(router)
