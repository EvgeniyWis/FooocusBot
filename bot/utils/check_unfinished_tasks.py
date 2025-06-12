import os
import json
from datetime import datetime

import redis.asyncio as aioredis

from logger import logger


class CheckUnfinishedTasks:
    """
    Класс для проверки и восстановления незавершенных задач 
    (генерации изображений, upscale изображений, генерации видео, faceswap) в Redis.
    Использует Redis для хранения и управления задачами.
    
    Attributes:
        redis_client (aioredis.Redis): Асинхронный клиент Redis.
        connected (bool): Флаг, указывающий на успешное подключение к Redis.
    
    Methods:
        init_redis(): Инициализирует соединение с Redis и проверяет его работоспособность.
        check_tasks(): Проверяет наличие незавершенных задач в Redis.
        append_new_task(task): Добавляет новую задачу в Redis.
        recover_unfinished_tasks(process_task_callback): Восстанавливает незавершенные задачи, вызывая callback для обработки каждой задачи.
    """
    
    def __init__(self, redis_client: aioredis.Redis) -> None:
        self.redis_client = redis_client
        self.connected = False

    async def init_redis(self) -> None:
        try:
            await self.redis_client.ping()
            logger.info("Redis connection is healthy.")
            self.connected = True
        except aioredis.ConnectionError as e:
            logger.error(f"Redis connection error: {e}")
            self.connected = False
            raise

    async def check_tasks(self) -> list:
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
     
    async def append_new_task(self, task) -> None:
        job_id = task.get("job_id")
        user_id = task.get("user_id")
        if not job_id or not user_id:
            logger.warning("No job_id or user_id in task")
            return
        key = f"task:{job_id}"
        task["created_at"] = task.get("created_at") or datetime.now().isoformat()
        task["status"] = task.get("status") or "in_progress"
        await self.redis_client.set(key, json.dumps(task))

    async def recover_unfinished_tasks(self, process_task_callback) -> None:
        tasks = await self.check_tasks()
        for task in tasks:
            if task.get("status") == "in_progress":
                logger.info(f"Recovering unfinished task: {task}")
                await process_task_callback(task)


r_password = os.getenv("REDIS_PASSWORD", "pass123")
r = aioredis.from_url(f"redis://:{r_password}@localhost:6380/0")
check_unfinished_tasks = CheckUnfinishedTasks(r)
# Для инициализации соединения с Redis вызови await check_unfinished_tasks.init_redis() при старте бота
