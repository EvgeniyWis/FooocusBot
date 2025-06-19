from aiogram.fsm.context import FSMContext

from bot.adapters.redis_task_storage_repository import key_for_image_block
from bot.logger import logger
from bot.settings import settings
from bot.storage import get_redis_storage


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
        redis_storage = get_redis_storage()
        await redis_storage.delete_task(
            settings.PROCESS_IMAGE_BLOCK_TASK,
            key_for_image_block(job_id),
        )

        return True
    except Exception as e:
        logger.error(
            f"Ошибка при очистке состояния для работы {job_id}: {str(e)}",
        )
        return False
