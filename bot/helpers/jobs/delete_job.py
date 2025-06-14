from aiogram.fsm.context import FSMContext

from bot.logger import logger
from bot.storage import get_task_service


async def delete_job(job_id: str, state: FSMContext) -> bool:
    """
    Удаление задачи из стейта и Redis

    Args:
        job_id (str): ID работы
        state (FSMContext): Контекст состояния

    Returns:
        bool: True, если задача успешно удалена, False в случае ошибки
    """

    # Удаляем id работы из стейта
    try:
        state_data = await state.get_data()
        image_generation_jobs = state_data.get("image_generation_jobs", [])

        # Находим и удаляем задачу по job_id
        image_generation_jobs = [
            job for job in image_generation_jobs if job["job_id"] != job_id
        ]
        await state.update_data(image_generation_jobs=image_generation_jobs)
        logger.info(
            f"Удаляем id работы {job_id} из стейта {image_generation_jobs}",
        )

        # Удаляем задачу из Redis
        task_service = get_task_service()
        await task_service.delete_task(job_id)

        return True
    except Exception as e:
        logger.error(
            f"Ошибка при очистке состояния для работы {job_id}: {str(e)}",
        )
        return False
