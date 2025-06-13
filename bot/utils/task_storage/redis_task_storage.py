import asyncio
import json
from typing import Any, Callable, Optional

import redis.asyncio as aioredis
from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.exceptions import TelegramAPIError, TelegramRetryAfter
from utils.task_storage.istorage import ITaskStorage
from utils.task_storage.redis_factory import create_redis_client
from logger import logger


class RedisTaskRepository(ITaskStorage):
    """
    Репозиторий для работы с отложенными задачами в Redis.
    Хранит и восстанавливает задачи генерации изображений.
    """

    def __init__(self, redis_client: Optional[aioredis.Redis] = None) -> None:
        # Используем фабрику для получения клиента, если не передан
        self.redis: aioredis.Redis = redis_client or create_redis_client()
        self._process_image_callback = None

    async def init_redis(self) -> None:
        """
        Проверяет доступность Redis.
        """
        try:
            await self.redis.ping()
            logger.info("[RedisTaskRepository] Redis is available")
        except Exception as e:
            logger.error(f"[RedisTaskRepository] Redis ping failed: {e}")
            raise

    async def add_task(
        self,
        job_id: str,
        user_id: int,
        job_type: str,
        model_name: str,
        setting_number: int,
        is_test_generation: bool,
        check_other_jobs: bool,
        message_id: int,
    ) -> None:
        """
        Сохраняет новую задачу в Redis. Если задача уже есть — пропускает.

        :param job_id: уникальный идентификатор задачи
        :param user_id: Telegram user_id
        :param job_type: тип задачи ("generate_image", "upscale" и т.д.)
        :param model_name: имя модели генерации
        :param setting_number: номер набора параметров
        :param is_test_generation: флаг тестовой генерации
        :param check_other_jobs: флаг проверки других задач
        :param message_id: идентификатор сообщения для восстановления
        """
        key = f"task:{job_id}"
        exists = await self.redis.exists(key)
        if exists:
            logger.warning(f"[RedisTaskRepository] Task {key} already exists, skip adding")
            return
        payload = {
            "job_id": job_id,
            "user_id": user_id,
            "job_type": job_type,
            "model_name": model_name,
            "setting_number": setting_number,
            "is_test_generation": is_test_generation,
            "check_other_jobs": check_other_jobs,
            "message_id": message_id,
        }
        data = json.dumps(payload)
        # Сохраняем на 24 часа
        await self.redis.set(key, data, ex=24 * 3600)
        logger.info(f"[RedisTaskRepository] Task saved: {key}")

    async def get_task(self, job_id: str) -> Optional[dict[str, Any]]:
        """
        Возвращает словарь задачи по job_id или None.
        """
        key = f"task:{job_id}"
        data = await self.redis.get(key)
        if not data:
            return None
        try:
            return json.loads(data)
        except Exception as e:
            logger.error(f"[RedisTaskRepository] Failed to decode task {key}: {e}")
            return None

    async def delete_task(self, job_id: str) -> None:
        """
        Удаляет задачу из Redis по job_id.
        """
        key = f"task:{job_id}"
        await self.redis.delete(key)
        logger.info(f"[RedisTaskRepository] Task deleted: {key}")

    async def recover_tasks(self, bot: Bot, state_storage, prefix: str = "task:") -> None:
        """
        Восстанавливает все задачи из Redis и проигрывает их.

        :param bot: экземпляр aiogram.Bot
        :param state_storage: хранилище FSMContext (RedisStorage)
        :param prefix: префикс ключей задач        
        """
        keys = await self.redis.keys(f"{prefix}*")
        for key in keys:
            job_id = key.decode().split("task:")[1]
            await self.replay_task(job_id, bot, state_storage)          

    async def replay_task(
        self,
        job_id: str,
        bot: Bot,
        state_storage,
    ) -> bool:
        """
        Воспроизводит задачу:
        - Получает payload из Redis
        - Создаёт FSMContext
        - Отправляет новое сообщение (или использует старое message_id для редактирования)
        - Запускает process_image_block
        """
        task = await self.get_task(job_id)
        if not task:
            logger.warning(f"[RedisTaskRepository] No task to replay: {job_id}")
            return False

        try:
            user_id = task["user_id"]
            chat_id = task["chat_id"]
            message_id = task["message_id"]

            # Восстановление FSMContext
            key = StorageKey(bot_id=bot.id, user_id=user_id, chat_id=chat_id)
            state = FSMContext(storage=state_storage, key=key)

            # Запускаем обработку блока
            success = await self._process_image_callback(
                job_id=task["job_id"],
                model_name=task["model_name"],
                setting_number=task["setting_number"],
                user_id=user_id,
                state=state,
                message_id=message_id,
                is_test_generation=task["is_test_generation"],
                checkOtherJobs=task["check_other_jobs"],
            )

            if success:
                await self.delete_task(job_id)
            return success

        except TelegramRetryAfter as e:
            logger.warning(f"[RedisTaskRepository] TelegramRetryAfter for {job_id}, retry in {e.timeout}s")
            await asyncio.sleep(e.timeout)
            return await self.replay_task(job_id, bot, state_storage)

        except TelegramAPIError as e:
            logger.error(f"[RedisTaskRepository] Telegram API error: {e}")
            return False

        except Exception as e:
            logger.error(f"[RedisTaskRepository] Error replaying {job_id}: {e}")
            return False
