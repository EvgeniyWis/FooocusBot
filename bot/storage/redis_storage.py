from typing import Optional

from redis import Redis

from bot.utils.adapters.redis_task_storage_repository import (
    RedisTaskStorageRepository,
)

_redis_storage_instance: Optional[RedisTaskStorageRepository] = None


async def init_redis_storage(redis_client: Redis) -> None:
    """
    Инициализирует Redis хранилище с переданным клиентом Redis.

    Args:
        redis_client: Клиент Redis для инициализации хранилища

    Raises:
        aioredis.RedisError: при ошибке подключения к Redis
    """
    global _redis_storage_instance
    _redis_storage_instance = RedisTaskStorageRepository(redis_client)
    await _redis_storage_instance.init_redis()


def get_redis_storage() -> RedisTaskStorageRepository:
    """
    Возвращает экземпляр Redis хранилища.

    Returns:
        RedisTaskStorageRepository: Экземпляр хранилища Redis

    Raises:
        RuntimeError: Если хранилище не было инициализировано.
    """
    if _redis_storage_instance is None:
        raise RuntimeError(
            "Redis хранилище не инициализировано. "
            "Сначала вызовите init_redis_storage().",
        )
    return _redis_storage_instance
