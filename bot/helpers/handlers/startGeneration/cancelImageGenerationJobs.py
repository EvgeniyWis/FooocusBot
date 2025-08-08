import asyncio

from aiogram.fsm.context import FSMContext

from bot.app.core.logging import logger
from bot.helpers.jobs import cancel_jobs


# Функция для отмены всех работ по генерации изображений
async def cancelImageGenerationJobs(state: FSMContext):
    # Отменяем все работы
    state_data = await state.get_data()
    image_generation_jobs = state_data.get("image_generation_jobs", [])

    logger.info(f"Отменяем работы: {image_generation_jobs} ({len(image_generation_jobs)})")

    if len(image_generation_jobs) > 0:
        await cancel_jobs(image_generation_jobs)
    else:
        return