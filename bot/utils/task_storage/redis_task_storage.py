import os
import json
from typing import Any

import redis.asyncio as aioredis

from logger import logger
from utils.task_storage.istorage import ITaskStorage


class RedisTaskStorage(ITaskStorage):
    """
    Класс для проверки и восстановления незавершенных задач 
    (генерации изображений, upscale изображений) в Redis.
    Использует Redis для хранения и управления задачами.

    Attributes:
        redis_client (aioredis.Redis): Асинхронный клиент Redis.
        connected (bool): Флаг, указывающий на успешное подключение к Redis.

    Methods:
        init_redis(): Инициализирует соединение с Redis и проверяет его работоспособность.
        get_tasks(): Проверяет наличие задач в Redis.
        append_task(task): Добавляет новую задачу в Redis.
        recover_tasks(process_task_callback): Возобновляет работу задач при помощи внешних ф-ций.
        delete_task(job_id): Удаляет задачу из Redis по заданному job_id.
    """

    def __init__(self, redis_client: aioredis.Redis) -> None:
        self.redis_client = redis_client
        self.connected = False

    async def init_redis(self) -> None:
        """
        Инициализирует соединение с Redis и проверяет его работоспособность.

        Raises:
            aioredis.ConnectionError: Если не удалось подключиться к Redis.
        """
        try:
            await self.redis_client.ping()
            logger.info("Redis connection is healthy.")
            self.connected = True
        except aioredis.ConnectionError as e:
            logger.error(f"Redis connection error: {e}")
            self.connected = False
            raise aioredis.ConnectionError(f"Redis connection error: {e}")

    async def get_tasks(self) -> list:
        """
        Проверяет наличие незавершенных задач в Redis.
        Возвращает список задач, которые были найдены в Redis.
        Если задачи не найдены, возвращает пустой список.

        Returns:
            list: Список незавершенных задач, найденных в Redis.

        Raises:
            aioredis.RedisError: Если произошла ошибка при взаимодействии с Redis.

        """
        unfinished_tasks = await self.redis_client.keys("task:*")
        logger.info(f"Checking unfinished tasks: {unfinished_tasks}")
        tasks = []
        for key in unfinished_tasks:
            data = await self.redis_client.get(key)
            if data:
                try:
                    task = json.loads(data)
                    tasks.append(task)
                except Exception as e:
                    logger.warning(f"Failed to decode task {key}: {e}")
        return tasks

    async def append_task(self, task: dict[str, Any]) -> None:
        """
        Добавляет новую задачу в Redis.
        Если ключ задачи уже существует, пропускает добавление.
        Если задача лежит в Redis более 24 часов, она будет удалена.

        Args:
            task (dict[str, Any]): Задача, которую нужно добавить в Redis.

        Raises:
            aioredis.ConnectionError: Если не удалось подключиться к Redis.
            aioredis.RedisError: Если произошла ошибка при взаимодействии с Redis.
            Exception: Если возникла неизвестная ошибка при добавлении задачи.
        """
        job_id = task.get("job_id")
        user_id = task.get("user_id")
        job_type = task.get("job_type")
        if not job_id or not user_id or not job_type:
            logger.warning("Нет job_id или user_id или job_type в задаче: %s", task)
            return
        key = f"task:{job_id}"
        try:
            # Проверка на дублирование ключа
            exists = await self.redis_client.exists(key)
            if exists:
                logger.warning(f"Задача с ключом {key} уже существует. Пропуск добавления.")
                return
            try:
                task_json = json.dumps(task)
            except (TypeError, ValueError) as e:
                logger.error(f"Ошибка сериализации задачи {task}: {e}")
                return
            await self.redis_client.set(key, task_json, ex=60 * 60 * 24)
            logger.info(f"Задача успешно добавлена в Redis: {key}")
        except aioredis.ConnectionError as e:
            logger.error(f"Ошибка соединения с Redis при добавлении задачи {key}: {e}")
            raise aioredis.ConnectionError(f"Ошибка соединения с Redis при добавлении задачи {key}: {e}")
        except aioredis.RedisError as e:
            logger.error(f"Ошибка Redis при добавлении задачи {key}: {e}")
            raise aioredis.RedisError(f"Ошибка Redis при добавлении задачи {key}: {e}")
        except Exception as e:
            logger.error(f"Неизвестная ошибка при добавлении задачи {key}: {e}")
            raise Exception(f"Неизвестная ошибка при добавлении задачи {key}: {e}")


    async def delete_task(self, job_id: str) -> None:
        """
        Удаляет задачу из Redis по заданному job_id.

        Args:
            job_id (str): Идентификатор задачи, которую нужно удалить.

        Raises:
            aioredis.ConnectionError: Если не удалось подключиться к Redis.
            aioredis.RedisError: Если произошла ошибка при взаимодействии с Redis.
        """
        key = f"task:{job_id}"
        try:
            await self.redis_client.delete(key)
            logger.info(f"Задача {key} успешно удалена из Redis.")
        except aioredis.ConnectionError as e:
            logger.error(f"Ошибка соединения с Redis при удалении задачи {key}: {e}")
            raise aioredis.ConnectionError(f"Ошибка соединения с Redis при удалении задачи {key}: {e}")
        except aioredis.RedisError as e:
            logger.error(f"Ошибка Redis при удалении задачи {key}: {e}")
            raise aioredis.RedisError(f"Ошибка Redis при удалении задачи {key}: {e}")

    async def recover_tasks(self, process_task_callback) -> None:
        tasks = await self.check_tasks()
        if tasks:
            for task in tasks:
                logger.info(f"Recovering unfinished task: {task}")
                await process_task_callback(task)
        else:
            logger.info("No unfinished tasks found in Redis.")
