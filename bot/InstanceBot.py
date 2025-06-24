from datetime import timedelta

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.redis import RedisStorage

from bot.config import get_current_tokens
from bot.factory.redis_factory import create_redis_client

# Получаем токен из config.py (где уже загружен .env файл)
tokens = get_current_tokens()
bot_token = tokens["BOT_API_TOKEN"]

if not bot_token:
    raise ValueError("BOT_API_TOKEN не найден в переменных окружения")

# Создаём бота
bot = Bot(
    token=bot_token,
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
