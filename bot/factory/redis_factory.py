import redis.asyncio as aioredis
from bot.app.config.settings import settings

_redis_client = None


def create_redis_client() -> aioredis.Redis:
    global _redis_client

    if _redis_client is None:
        _redis_client = aioredis.from_url(
            f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
        )
    return _redis_client
