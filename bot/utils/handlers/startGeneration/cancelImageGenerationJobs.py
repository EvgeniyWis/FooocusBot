import asyncio
from aiogram.fsm.context import FSMContext
from utils.jobs import cancelJobs

# Функция для отмены всех работ по генерации изображений
async def cancelImageGenerationJobs(state: FSMContext):
    # Отменяем все работы
    stateData = await state.get_data()
    await cancelJobs(stateData.get("image_generation_jobs", []))

    # Проверяем через 5 секунд, что все работы остановлены, а если нет, то делаем повторно
    await asyncio.sleep(5)
    stateData = await state.get_data()
    image_generation_jobs = stateData.get("image_generation_jobs", [])
    if len(image_generation_jobs) > 0:
        await cancelJobs(image_generation_jobs)