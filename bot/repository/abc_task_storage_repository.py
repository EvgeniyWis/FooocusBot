from abc import ABC, abstractmethod
from collections.abc import Awaitable
from typing import Callable, Optional

from aiogram import Bot
from aiogram.fsm.context import FSMContext

from bot.domain.entities.task import TaskDTO


class AbstractTaskStorageRepository(ABC):
    """
    Абстрактный репозиторий для работы с хранилищем задач.
    Определяет интерфейс для операций с задачами.
    """

    @abstractmethod
    async def add_task(self, task: TaskDTO) -> None:
        """
        Добавляет новую задачу в хранилище.

        Args:
            task: Объект задачи для сохранения
        """
        pass

    @abstractmethod
    async def get_task(self, job_id: str) -> Optional[TaskDTO]:
        """
        Получает задачу по её ID.

        Args:
            job_id: Уникальный идентификатор задачи

        Returns:
            Optional[TaskDTO]: Найденная задача или None
        """
        pass

    @abstractmethod
    async def delete_task(self, job_id: str) -> None:
        """
        Удаляет задачу из хранилища.

        Args:
            job_id: Уникальный идентификатор задачи
        """
        pass

    @abstractmethod
    async def recover_tasks(
        self,
        bot: Bot,
        state_storage: FSMContext,
    ) -> None:
        """
        Восстанавливает незавершенные задачи при перезапуске бота.

        Args:
            bot: Экземпляр бота
            state_storage: Контекст состояния FSM
        """
        pass

    def set_process_callback(self, callback: Callable[..., Awaitable[bool]]):
        """
        Устанавливает колбэк для обработки задач.

        Args:
            callback: Асинхронная функция для обработки задач
        """
        pass
