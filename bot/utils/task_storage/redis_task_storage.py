import json
from typing import Any, Callable, Awaitable

import redis.asyncio as aioredis
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from utils.task_storage.istorage import ITaskStorage
from utils.task_storage.redis_factory import create_redis_client
from logger import logger


ProcessImageCallback = Callable[..., Awaitable[bool]]


class RedisTaskRepository(ITaskStorage):
    """
    Репозиторий для управления списком задач в Redis (генерации изображений, upscale, faceswap).

    Сохраняет, восстанавливает и удаляет задачи пользователей.
    Позволяет повторно запускать задачи, если они не были обработаны.
    Использует асинхронный клиент Redis и интегрируется с aiogram FSMContext.
    """

    def __init__(self, redis_client: aioredis.Redis | None = None) -> None:
        """
        Инициализация репозитория задач.

        Args:
            redis_client (aioredis.Redis): Экземпляр асинхронного клиента Redis.
                Если не передан, будет создан новый через фабрику.
        """
        self.redis: aioredis.Redis = redis_client or create_redis_client()
        self._process_image_callback: ProcessImageCallback | None = None

    def set_process_callback(self, callback: ProcessImageCallback) -> None:
        """
        Устанавливает callback-функцию для обработки задач.

        Args:
            callback (ProcessImageCallback): Асинхронная функция для обработки задач.
        """
        self._process_image_callback = callback

    async def init_redis(self) -> None:
        """
        Инициализирует подключение к Redis, если это необходимо.

        Обычно вызывается при запуске приложения для проверки соединения.
        """
        try:
            await self.redis.ping()
            logger.info("Redis connection initialized.")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")

    async def add_task(self, task: dict[str, Any]) -> None:
        """
        Добавляет новую задачу в Redis.

        Args:
            task (dict[str, Any]): Словарь с параметрами задачи, должен содержать уникальный job_id.
        """
        job_id = task.get("job_id")
        if not job_id:
            logger.error("[RedisTaskRepository] Не указан job_id при добавлении задачи.")
            return
        await self.redis.set(f"task:{job_id}", json.dumps(task))
        logger.debug(f"Задача {job_id} добавлена в Redis.")

    async def get_task(self, job_id: str) -> dict[str, Any] | None:
        """
        Получает задачу из Redis по её идентификатору.

        Args:
            job_id (str): Уникальный идентификатор задачи.

        Returns:
            dict[str, Any] | None: Словарь с параметрами задачи или None, если задача не найдена.
        """
        data = await self.redis.get(f"task:{job_id}")
        if data is None:
            logger.warning(f"Задача {job_id} не найдена в Redis.")
            return None
        try:
            return json.loads(data)
        except Exception as e:
            logger.error(f"Ошибка при разборе задачи {job_id}: {e}")
            return None

    async def delete_task(self, job_id: str) -> None:
        """
        Удаляет задачу из Redis по её идентификатору.

        Args:
            job_id (str): Уникальный идентификатор задачи.
        """
        await self.redis.delete(f"task:{job_id}")
        logger.debug(f"Задача {job_id} удалена из Redis.")

    async def replay_task(
        self,
        job_id: str,
        bot: Bot,
        state_storage: Any,
    ) -> bool:
        """
        Восстанавливает и повторно запускает задачу по её идентификатору.

        Восстанавливает FSMContext пользователя и вызывает callback для обработки задач.

        Args:
            job_id (str): Уникальный идентификатор задачи.
            bot (Bot): Экземпляр Telegram-бота.
            state_storage (Any): Хранилище состояний FSM.

        Returns:
            bool: True, если задача успешно выполнена и удалена, иначе False.
        """
        task = await self.get_task(job_id)
        if not task:
            logger.warning(f"[RedisTaskRepository] Нет задачи для повторного запуска: {job_id}")
            return False

        try:
            user_id = task["user_id"]
            chat_id = task["chat_id"]
            message_id = task["message_id"]

            key = StorageKey(bot_id=bot.id, user_id=user_id, chat_id=chat_id)
            state = FSMContext(storage=state_storage, key=key)

            if not self._process_image_callback:
                logger.error("[RedisTaskRepository] Callback для генерации изображений не установлен.")
                return False

            success = await self._process_image_callback(
                job_id=task["job_id"],
                model_name=task["model_name"],
                setting_number=task["setting_number"],
                user_id=user_id,
                message_id=message_id,
                is_test_generation=task["is_test_generation"],
                checkOtherJobs=task["check_other_jobs"],
            )

            if success:
                await self.delete_task(job_id)
            return success

        except Exception as e:
            logger.error(f"[RedisTaskRepository] Ошибка при повторном запуске задачи {job_id}: {str(e)}", exc_info=True)
            return False