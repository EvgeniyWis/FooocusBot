from datetime import timedelta

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.redis import RedisStorage

from bot.app.config.settings import settings
from bot.factory.redis_factory import create_redis_client

# Создаём отдельные роутеры для каждого хендлера
commands_router = Router()
start_generation_router = Router()
randomizer_router = Router()
nsfw_video_router = Router()
video_generation_router = Router()
multi_image_router = Router()
img2video_router = Router()
magnific_upscale_router = Router()

bot = Bot(
    token=settings.BOT_API_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML"),
)

redis_client = create_redis_client()

storage = RedisStorage(
    redis=redis_client,
    state_ttl=timedelta(days=15),
    data_ttl=timedelta(days=3),
)

dp = Dispatcher(storage=storage)

bot.session = AiohttpSession(timeout=180)


# Подключаем роутеры к диспетчеру
dp.include_router(commands_router)
dp.include_router(start_generation_router)
dp.include_router(randomizer_router)
dp.include_router(nsfw_video_router)
dp.include_router(video_generation_router)
dp.include_router(multi_image_router)
dp.include_router(img2video_router)
dp.include_router(magnific_upscale_router) 