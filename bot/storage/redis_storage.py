"""
Redis storage module to avoid circular imports.
This module provides a centralized way to access the Redis task storage.
"""

from typing import Optional

from redis import Redis

from bot.utils.adapters.redis_task_storage_repository import (
    RedisTaskStorageRepository,
)

# This will hold the initialized Redis storage instance
_redis_storage_instance: Optional[RedisTaskStorageRepository] = None


def init_redis_storage(redis_client: Redis) -> None:
    """Initialize the Redis storage with a Redis client."""
    global _redis_storage_instance
    _redis_storage_instance = RedisTaskStorageRepository(redis_client)


def get_redis_storage() -> RedisTaskStorageRepository:
    """Get the Redis storage instance.

    Raises:
        RuntimeError: If the storage has not been initialized.
    """
    if _redis_storage_instance is None:
        raise RuntimeError(
            "Redis storage has not been initialized. "
            "Call init_redis_storage() first.",
        )
    return _redis_storage_instance
