from __future__ import annotations

import asyncio
import json
from collections.abc import Coroutine
from typing import Any, Callable

import redis.asyncio as aioredis
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from bot.domain.entities.task import TaskDTO
from bot.factory.redis_factory import create_redis_client
from bot.logger import logger
from bot.repository.abc_task_storage_repository import (
    AbstractTaskStorageRepository,
)

ProcessImageCallback: Any = Callable[..., Coroutine]


class RedisTaskStorageRepository(AbstractTaskStorageRepository):
    """
    Репозиторий для работы с задачами генерации, сохранёнными в Redis.
    """

    def __init__(
        self,
        redis_client: aioredis.Redis | None = None,
    ) -> None:
        """
        Инициализация RedisTaskRepository.

        Args:
            redis_client (Optional[aioredis.Redis]):
                Асинхронный клиент Redis. Если None, создаётся новый через create_redis_client().
        """
        self.redis: aioredis.Redis = redis_client or create_redis_client()
        self._callback: ProcessImageCallback | None = None

    def set_process_callback(self, callback: ProcessImageCallback) -> None:
        """
        Устанавливает функцию-обработчик для восстановленных задач.

        Args:
            callback (ProcessImageCallback):
                Асинхронная функция с параметрами (job_id, model_name, setting_number,
                user_id, state, message_id, is_test_generation, check_other_jobs),
                возвращающая True при успешной обработке.
        """
        self._callback = callback

    async def init_redis(self) -> None:
        """
        Проверяет соединение с Redis командой PING.

        Raises:
            aioredis.RedisError: при сбое PING.
        """
        await self.redis.ping()
        logger.info("Подключение к Redis установлено")

    async def add_task(
        self,
        task: TaskDTO,
    ) -> None:
        """
        Сохраняет новую задачу в Redis с проверкой существования.

        Метод создает уникальный ключ для задачи в формате "task:{job_id}"
        и сохраняет сериализованные данные задачи в Redis с TTL 24 часа.
        Если задача с таким ID уже существует, она не будет перезаписана.

        Args:
            task (TaskDTO): Объект задачи для сохранения

        Returns:
            None

        Raises:
            RedisError: Если возникают проблемы с подключением к Redis
        """
        key = f"task:{task.job_id}"
        if await self.redis.exists(key):
            logger.warning(
                f"Задача '{task.job_id}' уже существует, пропускаем",
            )
            return

        # Используем метод to_dict() для сериализации
        payload = task.to_dict()
        await self.redis.set(key, json.dumps(payload), ex=24 * 3600)
        logger.debug(f"Задача сохранена: {task.job_id}")

    async def get_task(self, job_id: str) -> TaskDTO | None:
        """
        Получает задачу по ID.

        Метод ищет задачу в Redis по её уникальному идентификатору,
        десериализует её из JSON и возвращает как объект TaskDTO.
        Если задача не найдена или JSON некорректен, возвращает None.

        Args:
            job_id (str): ID задачи

        Returns:
            Optional[TaskDTO]: Объект TaskDTO с данными задачи или None, если задача не найдена
        """
        key = f"task:{job_id}"
        task_data = await self.redis.get(key)
        if not task_data:
            return None

        task_dict = json.loads(task_data)
        return TaskDTO.from_dict(task_dict)

    async def delete_task(self, job_id: str) -> None:
        """
        Удаляет запись задачи из Redis.

        Удаляет задачу из хранилища Redis по её уникальному идентификатору.
        Ключ задачи формируется в формате "task:<job_id>".

        Args:
            job_id (str): Уникальный идентификатор задачи для удаления.

        Returns:
            None

        Raises:
            RedisError: В случае возникновения ошибки при работе с Redis.
        """

        await self.redis.delete(f"task:{job_id}")
        logger.debug(f"Задача удалена: {job_id}")

    async def replay_task(
        self,
        job_id: str,
        bot: Bot,
        state_storage,
    ) -> bool:
        """
        Восстанавливает FSMContext и вызывает callback для одной задачи.

        Args:
            job_id (str): Идентификатор задачи для восстановления.
            bot (Bot): Экземпляр бота Aiogram.
            state_storage: Бэкенд хранения состояний FSM.

        Returns:
            bool: True, если задача успешно обработана и удалена;
            False в противном случае.
        """

        task = await self.get_task(job_id)
        if not task:
            logger.warning(f"Нет задачи '{job_id}' для восстановления")
            return False
        if self._callback is None:
            logger.error("Callback для обработки задач не установлен")
            return False

        try:
            key = StorageKey(
                bot_id=bot.id,
                chat_id=task.chat_id,
                user_id=task.user_id,
            )
            state = FSMContext(storage=state_storage, key=key)

            success = await self._callback(
                job_id=task.job_id,
                model_name=task.model_name,
                setting_number=task.setting_number,
                user_id=task.user_id,
                state=state,
                message_id=task.message_id,
                is_test_generation=task.is_test_generation,
                checkOtherJobs=task.check_other_jobs,
                chat_id=task.chat_id,
            )
            if success:
                await self.delete_task(job_id)
            return success

        except AttributeError as e:
            logger.error(f"Некорректные данные в задаче '{job_id}': {e}")
            return False
        except Exception:
            logger.exception(f"Ошибка при восстановлении задачи '{job_id}'")
            return False

    async def recover_tasks(self, bot: Bot, state_storage) -> None:
        """
        Восстанавливает все незавершенные задачи из Redis после перезапуска бота.

        Метод ищет все ключи, начинающиеся с "task:", и пытается восстановить
        каждую задачу через метод replay_task. Если задача успешно восстановлена,
        она удаляется из Redis.

        Args:
            bot (Bot): Экземпляр бота Aiogram для контекста.
            state_storage: Бэкенд хранения состояний FSM.

        Returns:
            None

        Raises:
            RedisError: Если возникают проблемы с подключением к Redis
        """

        keys = await self.redis.keys("task:*")
        tasks = []
        for raw in keys:
            job_id = raw.decode().split(":", 1)[1]
            logger.info(f"Восстановление задачи: {job_id}")
            task = asyncio.create_task(
                self.replay_task(job_id, bot, state_storage),
            )
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)
