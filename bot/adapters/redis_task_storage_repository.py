from __future__ import annotations

import asyncio
import json
from typing import Callable

import redis.asyncio as aioredis
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from utils.task_storage.rebuild_callback_query_from_task import (
    rebuild_callback_query_from_task,
)

from bot.domain.entities.task import TaskImageBlockDTO, TaskProcessImageDTO
from bot.factory.redis_factory import create_redis_client
from bot.logger import logger


class RedisTaskStorageRepository:
    """
    Асинхронный репозиторий для работы с задачами генерации изображений в Redis.

    Предоставляет методы для сохранения, извлечения и управления задачами двух типов:
    - process_image: задачи обработки одного изображения
    - process_image_block: задачи обработки блока изображений

    Все задачи автоматически удаляются через 24 часа после создания.
    """

    def __init__(
        self,
        redis_client: aioredis.Redis | None = None,
    ) -> None:
        """
        Инициализирует репозиторий для работы с задачами в Redis.

        Args:
            redis_client:
                Существующий асинхронный клиент Redis.
                Если не указан, будет создан новый через create_redis_client().
                По умолчанию None.
        """
        self.redis: aioredis.Redis = redis_client or create_redis_client()
        self._callbacks: dict[str, Callable] = {}

    def set_process_callback(self, callback: Callable, job_type: str) -> None:
        """
        Регистрирует обработчик для указанного типа задач.

        Обработчик будет вызываться при восстановлении задач соответствующего типа.

        Args:
            callback:
                Асинхронная функция-обработчик, принимающая параметры задачи
            job_type:
                Тип задачи, для которого регистрируется обработчик.
                Допустимые значения: 'process_image' или 'process_image_block'

        Raises:
            ValueError: Если передан некорректный тип задачи
        """
        self._callbacks[job_type] = callback
        logger.info(f"Установлен обработчик для типа задачи: {job_type}")

    async def init_redis(self) -> None:
        """
        Проверяет работоспособность подключения к Redis.

        Raises:
            aioredis.RedisError:
                Если не удалось установить соединение с Redis
                или получить ответ на команду PING.

        Note:
            Вызывается автоматически при инициализации репозитория,
            но может быть вызван повторно для проверки соединения.
        """
        await self.redis.ping()
        logger.info("Подключение к Redis установлено")

    async def add_task_process_image_block(
        self,
        task_image_block: TaskImageBlockDTO,
    ) -> None:
        """
        Сохраняет задачу обработки блока изображений в Redis.

        Ключ задачи формируется по шаблону "task:{job_id}".
        Срок хранения задачи - 24 часа с момента создания.

        Args:
            task_image_block:
                DTO с данными задачи обработки блока изображений.
                Должен содержать уникальный job_id.

        Note:
            Если задача с таким job_id уже существует в Redis,
            новая запись создана не будет.
        """
        key = f"task:{task_image_block.job_id}"
        if await self.redis.exists(key):
            logger.warning(
                f"Задача '{task_image_block.job_id}' уже существует, пропускаем",
            )
            return

        payload = task_image_block.to_dict()
        await self.redis.set(key, json.dumps(payload), ex=24 * 3600)
        logger.debug(f"Задача сохранена: {task_image_block.job_id}")

    async def add_task_process_image(
        self,
        task_process_image: TaskProcessImageDTO,
    ) -> None:
        """
        Сохраняет задачу upscale/faceswap/save_drive изображения в Redis.

        Ключ формируется по шаблону "{user_id}:{image_index}:{model_name}".
        Срок хранения задачи - 24 часа с момента создания.

        Args:
            task_process_image:
                DTO с данными задачи обработки изображения.
                Должен содержать user_id, image_index и model_name.

        Note:
            Если задача с таким составным ключом уже существует в Redis,
            новая запись создана не будет.
        """
        key = f"{task_process_image.user_id}:{task_process_image.image_index}:{task_process_image.model_name}"
        if await self.redis.exists(key):
            logger.warning(f"Задача '{key}' уже существует, пропускаем")
            return

        payload = task_process_image.to_dict()
        await self.redis.set(key, json.dumps(payload), ex=24 * 3600)
        logger.debug(f"Задача сохранена: {key}")

    async def get_task_process_image_block(
        self,
        job_id: str,
    ) -> TaskImageBlockDTO | None:
        """
        Извлекает задачу обработки блока изображений по её идентификатору.

        Ищет задачу в Redis по ключу "task:{job_id}" и возвращает
        десериализованный объект TaskImageBlockDTO.

        Args:
            job_id:
                Уникальный идентификатор задачи.
                Должен соответствовать формату, используемому при сохранении.

        Returns:
                Объект задачи, если она найдена в Redis.
                None, если задача с указанным ID не существует.

        Note:
            Внутренние данные обратного вызова (callback_data) удаляются
            из результата при десериализации.
        """
        key = f"task:{job_id}"
        task_data = await self.redis.get(key)
        if not task_data:
            return None

        task_dict = json.loads(task_data)
        task_dict.pop("callback_data", None)
        return TaskImageBlockDTO.from_dict(task_dict)

    async def get_task_process_image(
        self,
        user_id: int,
        image_index: int,
        model_name: str,
    ) -> TaskProcessImageDTO | None:
        """
        Извлекает задачу upsacale/faceswap/save_drive по составному ключу.

        Формирует ключ в формате "{user_id}:{image_index}:{model_name}" и ищет
        соответствующую задачу в Redis. Возвращает десериализованный объект TaskProcessImageDTO.

        Args:
            user_id:
                Идентификатор пользователя, которому принадлежит задача.
            image_index:
                Порядковый номер изображения в рамках сессии пользователя.
            model_name:
                Название модели, используемой для обработки изображения.

        Returns:
                Объект задачи, если она найдена в Redis.
                None, если задача с указанными параметрами не существует.

        Note:
            В отличие от get_task_process_image_block, не удаляет
            callback_data из результата, так как он может потребоваться
            для восстановления контекста.
        """
        key = f"{user_id}:{image_index}:{model_name}"
        task_data = await self.redis.get(key)
        if not task_data:
            return None

        task_dict = json.loads(task_data)
        return TaskProcessImageDTO.from_dict(task_dict)

    async def delete_task_process_image_block(self, job_id: str) -> None:
        """
        Удаляет задачу обработки блока изображений из Redis.

        Удаляет задачу по ключу "task:{job_id}". Если задача не существует,
        операция завершается без ошибок.

        Args:
            job_id:
                Уникальный идентификатор задачи, которую необходимо удалить.

        Note:
            После удаления задачи, попытка её повторного получения
            с помощью get_task_process_image_block вернёт None.
        """
        await self.redis.delete(f"task:{job_id}")
        logger.debug(f"Задача удалена: {job_id}")

    async def delete_task_process_image(
        self,
        user_id: int,
        image_index: int,
        model_name: str,
    ) -> None:
        """
        Удаляет задачу upsacale/faceswap/save_drive из Redis по составному ключу.

        Формирует ключ в формате "{user_id}:{image_index}:{model_name}" и удаляет
        соответствующую запись из Redis. Если задача не существует, операция
        завершается без ошибок.

        Args:
            user_id:
                Идентификатор пользователя, которому принадлежит задача.
            image_index:
                Порядковый номер изображения в рамках сессии пользователя.
            model_name:
                Название модели, используемой для обработки изображения.

        Note:
            После удаления задачи, попытка её повторного получения
            с помощью get_task_process_image вернёт None.
        """
        key = f"{user_id}:{image_index}:{model_name}"
        await self.redis.delete(key)
        logger.debug(f"Задача удалена: {key}")

    async def replay_task(
        self,
        key: str,
        bot: Bot,
        state_storage: FSMContext,
    ) -> bool:
        """
        Восстанавливает контекст FSM и выполняет обработчик для указанной задачи.

        В зависимости от формата ключа задачи определяет её тип (process_image или process_image_block),
        загружает данные из Redis, восстанавливает контекст FSM и вызывает соответствующий обработчик.

        Args:
            key:
                Ключ задачи в Redis. Может быть двух форматов:
                - "task:{job_id}" для задач типа process_image_block
                - "{user_id}:{image_index}:{model_name}" для задач типа process_image
            bot:
                Экземпляр бота Aiogram, используемый для восстановления контекста.
            state_storage:
                Хранилище состояний FSM, используемое для восстановления контекста.

        Returns:
            True - если задача успешно обработана и удалена из Redis.
            False - если возникла ошибка или обработчик не найден.

        Note:
            В случае успешной обработки задача автоматически удаляется из Redis.
            Для задач process_image используется вспомогательная функция
            rebuild_callback_query_from_task для восстановления callback-запроса.
        """
        try:
            if (
                ":" in key
                and key.count(":") == 2
                and not key.startswith("task:")
            ):
                task_type = "process_image"
                try:
                    user_id, image_index, model_name = key.split(":", 2)
                    task = await self.get_task_process_image(
                        int(user_id),
                        int(image_index),
                        model_name,
                    )
                    if not task:
                        logger.warning(
                            f"Не найдена задача process_image: {key}",
                        )
                        return False
                except (ValueError, AttributeError) as e:
                    logger.error(
                        f"Неверный формат ключа задачи process_image '{key}': {e}",
                    )
                    return False
            else:
                task_type = "process_image_block"
                task_key = (
                    key.split(":", 1)[1] if key.startswith("task:") else key
                )
                task = await self.get_task_process_image_block(task_key)
                if not task:
                    logger.warning(
                        f"Не найдена задача process_image_block: {task_key}",
                    )
                    return False

            callback = self._callbacks.get(task_type)
            if not callback:
                logger.error(
                    f"Не найден обработчик для типа задачи: {task_type}",
                )
                return False

            key_storage = StorageKey(
                bot_id=bot.id,
                chat_id=task.chat_id,
                user_id=task.user_id,
            )
            state = FSMContext(storage=state_storage, key=key_storage)

            if task_type == "process_image_block":
                success = await callback(
                    job_id=task.job_id,
                    model_name=task.model_name,
                    setting_number=task.setting_number,
                    user_id=task.user_id,
                    state=state,
                    message_id=task.message_id,
                    is_test_generation=getattr(
                        task,
                        "is_test_generation",
                        False,
                    ),
                    checkOtherJobs=getattr(task, "check_other_jobs", False),
                    chat_id=task.chat_id,
                )
                if success:
                    await self.delete_task_process_image_block(task.job_id)
            else:
                fake_call = rebuild_callback_query_from_task(task)
                success = await callback(
                    call=fake_call,
                    state=state,
                    model_name=task.model_name,
                    image_index=task.image_index,
                )
                if success:
                    await self.delete_task_process_image(
                        task.user_id,
                        task.image_index,
                        task.model_name,
                    )

            return bool(success)

        except Exception as e:
            logger.exception(f"Ошибка при обработке задачи {key}: {str(e)}")
            return False

    async def recover_tasks(self, bot: Bot, state_storage: FSMContext) -> None:
        """
        Восстанавливает все незавершенные задачи из Redis после перезапуска бота.

        Находит все сохранённые задачи в Redis (как process_image, так и process_image_block),
        и для каждой из них асинхронно запускает процесс восстановления через replay_task.

        Args:
            bot:
                Экземпляр бота Aiogram, передаваемый в replay_task.
            state_storage:
                Хранилище состояний FSM, используемое для восстановления контекста.

        Note:
            - Игнорирует задачи, для которых не зарегистрирован обработчик.
            - Обрабатывает задачи конкурентно с помощью asyncio.gather.
            - Логирует статистику по успешным и неудачным попыткам восстановления.
            - Выводит предупреждение, если не найдено ни одного обработчика задач.
        """
        if not self._callbacks:
            logger.warning("Нет зарегистрированных обработчиков задач")
            return

        task_keys = await self.redis.keys("task:*")
        all_process_keys = await self.redis.keys("*:*:*")
        process_keys = [
            k
            for k in all_process_keys
            if k.count(b":") == 2 and not k.startswith(b"task:")
        ]
        all_keys = task_keys + process_keys

        if not all_keys:
            logger.info("Незавершенных задач для восстановления не найдено")
            return

        logger.info(f"Найдено {len(all_keys)} задач для восстановления")

        tasks = []
        for raw in all_keys:
            key_str = raw.decode()
            logger.info(f"Планируем восстановление задачи: {key_str}")
            task = self.replay_task(key_str, bot, state_storage)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        success_count = sum(1 for r in results if r is True)
        error_count = sum(
            1 for r in results if r is False or isinstance(r, Exception)
        )

        logger.info(
            f"Восстановление завершено. Успешно: {success_count}, Ошибок: {error_count}, Всего: {len(all_keys)}",
        )
