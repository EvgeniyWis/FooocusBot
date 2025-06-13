from aiogram.fsm.context import FSMContext
from logger import logger
from RunBot import redis_task_storage

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
        stateData = await state.get_data()
        image_generation_jobs = stateData.get("image_generation_jobs", [])
        
        # Находим и удаляем задачу по job_id
        image_generation_jobs = [job for job in image_generation_jobs if job['job_id'] != job_id]
        await state.update_data(image_generation_jobs=image_generation_jobs)
        logger.info(f"Удаляем id работы {job_id} из стейта {image_generation_jobs}")
        
        # Удаляем задачу из Redis
        await redis_task_storage.delete_task(job_id)

        return True
    except Exception as e:
        logger.error(f"Ошибка при очистке состояния для работы {job_id}: {str(e)}")
        return False