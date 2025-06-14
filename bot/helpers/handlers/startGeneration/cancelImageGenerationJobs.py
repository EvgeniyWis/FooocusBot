import asyncio

from aiogram.fsm.context import FSMContext

from bot.logger import logger
from bot.helpers.jobs import cancel_jobs


# Функция для отмены всех работ по генерации изображений
async def cancelImageGenerationJobs(state: FSMContext):
    # Отменяем все работы
    stateData = await state.get_data()
    image_generation_jobs = stateData.get("image_generation_jobs", [])

    logger.info(f"Отменяем работы: {image_generation_jobs}")

    if len(image_generation_jobs) > 0:
        await cancel_jobs(image_generation_jobs)
    else:
        return

    # Проверяем через 10 секунд, что все работы остановлены, а если нет, то делаем повторно
    await asyncio.sleep(10)
    stateData = await state.get_data()
    image_generation_jobs = stateData.get("image_generation_jobs", [])

    if len(image_generation_jobs) > 0:
        await cancel_jobs(image_generation_jobs)
