from typing import Optional, TypeVar, Type, Any

from redis import Redis

from bot.adapters.redis_task_storage_repository import RedisTaskStorageRepository
from bot.services.task_services import TaskService

T = TypeVar('T')

_redis_storage_instance: Optional[RedisTaskStorageRepository] = None
_task_service_instance: Optional[TaskService] = None


def get_service(service_class: Type[T], *args: Any, **kwargs: Any) -> T:
    """
    Фабрика для получения экземпляров сервисов с зависимостями.
    
    Args:
        service_class: Класс сервиса
        *args: Позиционные аргументы для конструктора
        **kwargs: Именованные аргументы для конструктора
        
    Returns:
        Экземпляр запрошенного сервиса
    """
    return service_class(*args, **kwargs)


async def init_redis_storage(redis_client: Redis) -> None:
    """
    Инициализирует Redis хранилище и сервисы.

    Args:
        redis_client: Клиент Redis для инициализации хранилища

    Raises:
        aioredis.RedisError: при ошибке подключения к Redis
    """
    global _redis_storage_instance, _task_service_instance
    
    # Инициализируем репозиторий
    _redis_storage_instance = RedisTaskStorageRepository(redis_client)
    await _redis_storage_instance.init_redis()
    
    # Инициализируем сервис задач
    _task_service_instance = get_service(TaskService, _redis_storage_instance)


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
            "Сначала вызовите init_redis_storage()."
        )
    return _redis_storage_instance


def get_task_service() -> TaskService:
    """
    Возвращает экземпляр сервиса задач.

    Returns:
        TaskService: Экземпляр сервиса задач

    Raises:
        RuntimeError: Если сервис не был инициализирован.
    """
    if _task_service_instance is None:
        raise RuntimeError(
            "Сервис задач не инициализирован. "
            "Сначала вызовите init_redis_storage()."
        )
    return _task_service_instance
