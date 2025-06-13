from __future__ import annotations

import json
from typing import Any, Coroutine, Callable

import redis.asyncio as aioredis
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from utils.task_storage.istorage import ITaskStorage
from utils.task_storage.redis_factory import create_redis_client
from logger import logger


ProcessImageCallback: Any = Callable[..., Coroutine]

class RedisTaskRepository(ITaskStorage):
    """
    Репозиторий для работы с задачами генерации, сохранёнными в Redis.

    - Сохраняет данные задачи под ключом "task:{job_id}" с TTL 24 часа.
    - Восстанавливает незавершённые задачи после перезапуска.
    - Вызывает зарегистрированный callback для обработки каждой задачи.
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
        job_id: str,
        user_id: int,
        message_id: int,
        model_name: str,
        setting_number: int,
        job_type: str,
        is_test_generation: bool,
        check_other_jobs: bool,
        chat_id: int,
    ) -> None:
        """
        Сохраняет новую задачу в Redis, если она ещё не существует.

        Args:
            job_id (str): Уникальный идентификатор задачи.
            user_id (int): ID пользователя Telegram, создающего задачу.
            message_id (int): ID сообщения для редактирования или ответа.
            model_name (str): Название модели генерации.
            setting_number (int): Номер набора параметров.
            job_type (str): Тип задачи (например, "generate_image").
            is_test_generation (bool): Флаг тестового режима.
            check_other_jobs (bool): Флаг обновления стейта по другим задачам.
            chat_id (int): ID чата.

        Returns:
            None
        """
        key = f"task:{job_id}"
        if await self.redis.exists(key):
            logger.warning(f"Задача '{job_id}' уже существует, пропускаем")
            return

        payload = {
            "job_id": job_id,
            "user_id": user_id,
            "message_id": message_id,
            "model_name": model_name,
            "setting_number": setting_number,
            "job_type": job_type,
            "chat_id": chat_id,
            "is_test_generation": is_test_generation,
            "check_other_jobs": check_other_jobs,
        }
        await self.redis.set(key, json.dumps(payload), ex=24 * 3600)
        logger.debug(f"Задача сохранена: {job_id}")

    async def get_task(self, job_id: str) -> dict[str, Any] | None:
        """
        Получает данные задачи из Redis.

        Args:
            job_id (str): Уникальный идентификатор задачи.

        Returns:
            dict[str, Any] | None: Десериализованные данные задачи или None,
            если ключ отсутствует или JSON некорректен.
        """
        key = f"task:{job_id}"
        raw = await self.redis.get(key)
        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            logger.error(f"Не удалось распарсить JSON задачи '{job_id}'")
            return None

    async def delete_task(self, job_id: str) -> None:
        """
        Удаляет запись задачи из Redis.

        Args:
            job_id (str): Уникальный идентификатор задачи.

        Returns:
            None
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
            user_id = task['user_id']
            chat_id = task['chat_id']
            message_id = task['message_id']

            key = StorageKey(
                bot_id=bot.id,
                chat_id=chat_id,
                user_id=user_id,
            )
            state = FSMContext(storage=state_storage, key=key)

            success = await self._callback(
                task['job_id'],
                task['model_name'],
                task['setting_number'],
                user_id,
                state,
                message_id,
                task['is_test_generation'],
                task['check_other_jobs'],
            )
            if success:
                await self.delete_task(job_id)
            return success

        except KeyError as e:
            logger.error(f"В данных задачи '{job_id}' отсутствует поле: {e}")
            return False
        except Exception:
            logger.exception(f"Ошибка при восстановлении задачи '{job_id}'")
            return False

    async def recover_tasks(self, bot: Bot, state_storage) -> None:
        """
        Перебирает все задачи в Redis и пытается их восстановить.

        Args:
            bot (Bot): Экземпляр бота Aiogram для контекста.
            state_storage: Бэкенд хранения состояний FSM.

        Returns:
            None
        """
        keys = await self.redis.keys('task:*')
        for raw in keys:
            job_id = raw.decode().split(':', 1)[1]
            logger.info(f"Восстановление задачи: {job_id}")
            await self.replay_task(job_id, bot, state_storage)
