import os
import redis.asyncio as aioredis


_redis_client = None

def create_redis_client() -> aioredis.Redis:
    """
    Создает и возвращает асинхронного Redis-клиента.
    Конфигурация берется из переменных окружения.
    Если клиент уже создан, возвращает существующий экземпляр.
    
    :return: Асинхронный Redis-клиент.
    """
    global _redis_client
    redis_password = os.getenv("REDIS_PASSWORD", "pass123")
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = os.getenv("REDIS_PORT", "6380")
    redis_db = os.getenv("REDIS_DB", "0")

    if _redis_client is None:
       _redis_client = aioredis.from_url(f"redis://:{redis_password}@{redis_host}:{redis_port}/{redis_db}")
    return _redis_client

