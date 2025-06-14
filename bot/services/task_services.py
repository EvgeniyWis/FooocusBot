from typing import Optional, Callable, Awaitable, Any

from aiogram import Bot
from aiogram.fsm.context import FSMContext

from bot.domain.entities.task import TaskDTO
from bot.repository.abc_task_storage_repository import AbstractTaskStorageRepository


class TaskService:
    """
    Сервис для работы с задачами генерации.
    Предоставляет бизнес-логику поверх репозитория задач.
    """

    def __init__(self, repository: AbstractTaskStorageRepository):
        """
        Инициализация сервиса задач.

        Args:
            repository: Репозиторий для работы с хранилищем задач
        """
        self._repo = repository

    async def create_task(
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
    ) -> TaskDTO:
        """
        Создает и сохраняет новую задачу.

        Args:
            job_id: Уникальный идентификатор задачи
            user_id: ID пользователя Telegram
            message_id: ID сообщения для обновления
            model_name: Название модели генерации
            setting_number: Номер настройки
            job_type: Тип задачи (например, 'image_generation')
            is_test_generation: Флаг тестовой генерации
            check_other_jobs: Флаг проверки других задач
            chat_id: ID чата

        Returns:
            Созданный DTO задачи
        """
        task = TaskDTO(
            job_id=job_id,
            user_id=user_id,
            message_id=message_id,
            model_name=model_name,
            setting_number=setting_number,
            job_type=job_type,
            is_test_generation=is_test_generation,
            check_other_jobs=check_other_jobs,
            chat_id=chat_id,
        )
        await self._repo.add_task(task)
        return task

    async def get_task(self, job_id: str) -> Optional[TaskDTO]:
        """
        Получает задачу по ID.

        Args:
            job_id: Уникальный идентификатор задачи

        Returns:
            DTO задачи или None, если задача не найдена
        """
        return await self._repo.get_task(job_id)

    async def delete_task(self, job_id: str) -> None:
        """
        Удаляет задачу по ID.

        Args:
            job_id: Уникальный идентификатор задачи
        """
        await self._repo.delete_task(job_id)

    async def recover_tasks(
        self,
        bot: Bot,
        state_storage: FSMContext,
        process_callback: Callable[..., Awaitable[bool]]
    ) -> None:
        """
        Восстанавливает незавершенные задачи при перезапуске бота.

        Args:
            bot: Экземпляр бота
            state_storage: Контекст состояния FSM
            process_callback: Функция для обработки восстановленных задач
        """
        if hasattr(self._repo, 'set_process_callback'):
            self._repo.set_process_callback(process_callback)
        await self._repo.recover_tasks(bot, state_storage)

    def set_process_callback(self, callback: Callable[..., Awaitable[bool]]) -> None:
        """
        Устанавливает колбэк для обработки задач.

        Args:
            callback: Асинхронная функция для обработки задач
        """
        if hasattr(self._repo, 'set_process_callback'):
            self._repo.set_process_callback(callback)
