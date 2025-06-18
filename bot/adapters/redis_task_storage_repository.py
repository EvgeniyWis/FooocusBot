import asyncio
import json
import time
from typing import Callable, TypeVar

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from config import PROCESS_VIDEO_TASK
from factory.redis_factory import create_redis_client

from bot.config import PROCESS_IMAGE_BLOCK_TASK, PROCESS_IMAGE_TASK
from bot.domain.entities.task import (
    TaskImageBlockDTO,
    TaskProcessImageDTO,
    TaskProcessVideoDTO,
)
from bot.logger import logger
from bot.utils.task_storage.rebuild_callback_query_from_task import (
    rebuild_callback_query_from_task,
)

T = TypeVar("T")


def key_for_image_block(job_id: str) -> str:
    return f"{PROCESS_IMAGE_BLOCK_TASK}:{job_id}"


def key_for_image(user_id: int, image_index: int, model_name: str) -> str:
    return f"{PROCESS_IMAGE_TASK}:{user_id}:{image_index}:{model_name}"


def key_for_video(
    type_for_video: str,
    user_id: int,
    image_url: str,
    model_name: str,
) -> str:
    return f"{PROCESS_VIDEO_TASK}:{type_for_video}:{user_id}:{image_url}:{model_name}"


class RedisTaskStorageRepository:
    """
    Репозиторий для хранения и управления фоновыми задачами в Redis.

    Предоставляет интерфейс для сохранения, извлечения и управления
    длительными задачами с использованием Redis в качестве хранилища.
    Поддерживает автоматическое восстановление задач при перезапуске системы.
    """

    def __init__(self, redis_client=None):
        """Инициализация репозитория задач Redis.

        Params:
            - redis_client: Опциональный клиент Redis. Если не указан,
                        будет создан новый клиент через фабрику.
        """
        self.redis = redis_client or create_redis_client()
        self._callbacks: dict[str, Callable] = {}
        logger.info(f"Инициализирован {self.__class__.__name__}")

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

    async def add_task(self, task_type: str, dto) -> bool:
        """Добавляет новую задачу в хранилище Redis.

        Params:
            - task_type: Тип задачи (например, 'process_image', 'process_video')
            - dto: Объект передачи данных с деталями задачи

        Returns:
            bool: True если задача успешно добавлена, иначе False
        """
        start_time = time.monotonic()
        key = self._build_key(task_type, dto)
        try:
            exists = await self.redis.exists(key)
            if exists:
                logger.info(
                    f"Задача с ключом {key} уже существует, пропускаем добавление",
                )
                return False

            serialized = json.dumps(dto.__dict__)
            ttl = 24 * 60 * 60  # 24 часа
            result = await self.redis.setex(key, ttl, serialized)

            logger.info(
                f"Задача добавлена | тип={task_type} | ключ={key} | "
                f"время={(time.monotonic() - start_time):.3f}с",
            )
            return result
        except Exception as e:
            logger.error(
                f"Ошибка при добавлении задачи | тип={task_type} | ключ={key} | ошибка={str(e)}",
                exc_info=True,
            )
            return False

    async def get_task(
        self,
        task_type: str,
        key: str,
    ) -> TaskImageBlockDTO | TaskProcessImageDTO | TaskProcessVideoDTO | None:
        """Извлекает задачу из хранилища Redis.

        Params:
            - task_type: Тип задачи
            - key: Ключ Redis задачи

        Returns:
            TaskImageBlockDTO | TaskProcessImageDTO | TaskProcessVideoDTO | None:
                DTO задачи если найдена, иначе None
        """
        start_time = time.monotonic()
        try:
            data = await self.redis.get(key)
            if not data:
                logger.debug(f"Задача не найдена | ключ={key}")
                return None

            dto_class = self._get_dto_class(task_type)
            task_data = json.loads(data)
            task = dto_class(**task_data)

            logger.debug(
                f"Задача получена | тип={task_type} | ключ={key} | "
                f"время={(time.monotonic() - start_time):.3f}с",
            )
            return task
        except Exception as e:
            logger.error(
                f"Ошибка при получении задачи | ключ={key} | ошибка={str(e)}",
                exc_info=True,
            )
            return None

    async def delete_task(self, task_type: str, key) -> bool:
        """Удаляет задачу из хранилища Redis.

        Params:
            - task_type: Тип задачи
            - key: Ключ Redis задачи или DTO объект задачи

        Returns:
            bool: True если задача успешно удалена, иначе False
        """
        try:
            # Если передан DTO объект, а не ключ, строим ключ
            if not isinstance(key, str):
                redis_key = self._build_key(task_type, key)
            else:
                redis_key = key

            result = await self.redis.delete(redis_key)
            if result > 0:
                logger.info(
                    f"Задача удалена | тип={task_type} | ключ={redis_key}",
                )
                return True
            logger.warning(
                f"Задача не найдена для удаления | ключ={redis_key}",
            )
            return False
        except Exception as e:
            logger.error(
                f"Ошибка при удалении задачи | тип={task_type} | ключ={key} | ошибка={str(e)}",
                exc_info=True,
            )
            return False

    async def replay_task(
        self,
        key: str,
        bot: Bot,
        state_storage: FSMContext,
    ) -> bool:
        """Воспроизводит задачу из хранилища Redis.

        Метод извлекает задачу, восстанавливает её состояние и выполняет
        соответствующий обработчик.

        Params:
            - key: Ключ Redis задачи
            - bot: Экземпляр бота
            - state_storage: Хранилище состояний FSM

        Returns:
            bool: True если задача успешно воспроизведена, иначе False
        """
        logger.info(f"Попытка воспроизвести задачу | ключ={key}")
        start_time = time.monotonic()

        try:
            task_type = self._detect_task_type_by_prefix(key)
            logger.debug(
                f"Определен тип задачи | тип={task_type} | ключ={key}",
            )

            task = await self.get_task(task_type, key)
            if not task:
                logger.warning(f"Задача не найдена в хранилище | ключ={key}")
                return False

            callback = self._callbacks.get(task_type)
            if not callback:
                logger.error(f"Нет обработчика для задачи | тип={task_type}")
                return False

            key_storage = StorageKey(
                bot_id=bot.id,
                chat_id=task.chat_id,
                user_id=task.user_id,
            )
            state = FSMContext(storage=state_storage, key=key_storage)

            # Вызов соответствующего обработчика
            match task_type:
                case "process_image_block":
                    logger.info(
                        f"Воспроизведение задачи блока | job_id={task.job_id}",
                    )
                    success = await callback(
                        job_id=task.job_id,
                        model_name=task.model_name,
                        setting_number=task.setting_number,
                        is_test_generation=getattr(
                            task,
                            "is_test_generation",
                            False,
                        ),
                        checkOtherJobs=getattr(
                            task,
                            "check_other_jobs",
                            False,
                        ),
                        chat_id=task.chat_id,
                        state=state,
                        user_id=task.user_id,
                        message_id=task.message_id,
                    )
                case "process_image":
                    logger.info(
                        f"Воспроизведение задачи изображения | user_id={task.user_id}",
                    )
                    call = rebuild_callback_query_from_task(
                        task,
                    )
                    success = await callback(
                        model_name=task.model_name,
                        image_index=task.image_index,
                        state=state,
                        call=call,
                    )
                case "process_video":
                    logger.info(
                        f"Воспроизведение задачи видео | user_id={task.user_id}",
                    )
                    call = rebuild_callback_query_from_task(
                        task,
                    )
                    success = await callback(
                        call=call,
                        model_name=task.model_name,
                        prompt=task.prompt,
                        type_for_video_generation=task.type_for_video_generation,
                        image_url=task.image_url,
                        state=state,
                    )
                case _:
                    logger.error(f"Неизвестный тип задачи: {task_type}")
                    return False

            if success:
                await self.delete_task(task_type, key)

            return bool(success)

        except Exception as e:
            logger.error(
                f"Ошибка при воспроизведении задачи | ключ={key} | ошибка={str(e)}",
                exc_info=True,
            )
            return False

    async def recover_tasks(self, bot: Bot, state_storage: FSMContext) -> None:
        """Восстанавливает и воспроизводит все незавершенные задачи из Redis.

        Метод сканирует Redis на наличие задач с известными префиксами
        и пытается восстановить и воспроизвести их.

        Params:
            - bot: Экземпляр бота
            - state_storage: Хранилище состояний FSM
        """
        start_time = time.monotonic()
        restored = 0
        failed = 0

        prefixes = [
            PROCESS_IMAGE_BLOCK_TASK,
            PROCESS_IMAGE_TASK,
            PROCESS_VIDEO_TASK,
        ]

        tasks = []
        for prefix in prefixes:
            try:
                async for key in self.redis.scan_iter(match=f"{prefix}:*"):
                    key_str = key.decode() if isinstance(key, bytes) else key
                    logger.info(
                        f"Найдена задача для восстановления | ключ={key_str}",
                    )
                    tasks.append(
                        asyncio.create_task(
                            self._safe_replay_task(
                                key_str,
                                bot,
                                state_storage,
                            ),
                        ),
                    )
            except Exception as e:
                logger.error(
                    f"Ошибка при сканировании задач с префиксом {prefix}: {str(e)}",
                    exc_info=True,
                )

        if tasks:
            logger.info(f"Восстановление {len(tasks)} задач...")
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    logger.error(
                        "Ошибка при восстановлении задачи",
                        exc_info=result,
                    )
                    failed += 1
                elif result:
                    restored += 1
                else:
                    failed += 1

    async def _safe_replay_task(
        self,
        key: str,
        bot: Bot,
        state_storage: FSMContext,
    ) -> bool:
        """Безопасно воспроизводит одну задачу с обработкой ошибок.

        Params:
            - key: Ключ Redis задачи
            - bot: Экземпляр бота
            - state_storage: Хранилище состояний FSM

        Returns:
            bool: True если задача успешно воспроизведена, иначе False
        """
        try:
            return await self.replay_task(key, bot, state_storage)
        except Exception as e:
            logger.error(
                f"Критическая ошибка при восстановлении задачи | ключ={key} | ошибка={str(e)}",
                exc_info=True,
            )
            return False

    def _detect_task_type_by_prefix(self, key: str) -> str:
        """Определяет тип задачи по префиксу ключа.

        Params:
            - key: Ключ Redis задачи

        Returns:
            - str: Тип задачи

        Exceptions:
            - ValueError: Если префикс ключа не соответствует ни одному известному типу
        """
        if key.startswith(PROCESS_IMAGE_BLOCK_TASK):
            return "process_image_block"
        elif key.startswith(PROCESS_IMAGE_TASK):
            return "process_image"
        elif key.startswith(PROCESS_VIDEO_TASK):
            return "process_video"
        else:
            error_msg = f"Неизвестный префикс ключа задачи: {key}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    def _get_dto_class(self, task_type: str):
        """Возвращает класс DTO для указанного типа задачи.

        Params:
            - task_type: Тип задачи

        Returns:
            Type: Класс DTO

        Exceptions:
            - ValueError: Если тип задачи неизвестен
        """
        match task_type:
            case "process_image_block":
                return TaskImageBlockDTO
            case "process_image":
                return TaskProcessImageDTO
            case "process_video":
                return TaskProcessVideoDTO
            case _:
                error_msg = f"Неизвестный тип задачи: {task_type}"
                logger.error(error_msg)
                raise ValueError(error_msg)

    def _build_key(self, task_type: str, dto) -> str:
        """Строит ключ Redis на основе типа задачи и DTO.

        Params:
            - task_type: Тип задачи
            - dto: Объект передачи данных с деталями задачи

        Returns:
            str: Сформированный ключ Redis

        Exceptions:
            - ValueError: Если тип задачи неизвестен
        """
        try:
            if task_type == "process_image_block":
                return key_for_image_block(dto.job_id)
            elif task_type == "process_image":
                return key_for_image(
                    dto.user_id,
                    dto.image_index,
                    dto.model_name,
                )
            elif task_type == "process_video":
                return key_for_video(
                    dto.type_for_video_generation,
                    dto.user_id,
                    dto.image_url,
                    dto.model_name,
                )
            else:
                raise ValueError(f"Неизвестный тип задачи: {task_type}")
        except Exception as e:
            logger.error(
                f"Ошибка при построении ключа | тип={task_type} | ошибка={str(e)}",
            )
            raise

    def set_process_callback(self, callback: Callable, task_type: str) -> None:
        """Устанавливает обработчик для определенного типа задачи.

        Params:
            - callback: Функция-обработчик
            - task_type: Тип задачи, для которой устанавливается обработчик
        """
        self._callbacks[task_type] = callback
        logger.info(
            f"Установлен обработчик для типа задачи | тип={task_type}",
        )
