from typing import Optional

from redis import Redis

from bot.adapters.redis_task_storage_repository import (
    RedisTaskStorageRepository,
)

_redis_storage_instance: Optional[RedisTaskStorageRepository] = None


async def init_redis_storage(redis_client: Redis) -> None:
    global _redis_storage_instance

    _redis_storage_instance = RedisTaskStorageRepository(redis_client)
    await _redis_storage_instance.init_redis()


def get_redis_storage() -> RedisTaskStorageRepository:
    if _redis_storage_instance is None:
        raise RuntimeError(
            "Redis хранилище не инициализировано. "
            "Сначала вызовите инициализатор хранилища.",
        )
    return _redis_storage_instance
