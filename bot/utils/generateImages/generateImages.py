from utils.generateImages.generateImage import generateImage
from utils.generateImages.data_array import add_root_prompt
from logger import logger
from aiogram import types
import asyncio
from aiogram.fsm.context import FSMContext


# Функция для генерации изображений с помощью API
async def generateImages(prompt: str, message: types.Message, state: FSMContext):
    # Прибавляем к каждому элементу массива корневой промпт
    data_array = add_root_prompt(prompt)

    # Генерируем изображения по всем элементам массива
    jobs = {}
    await state.update_data(jobs=jobs)

    async def process_image(data):
        try:
            logger.info(f"Генерация изображения с изначальным промптом: {data['input']['prompt']}")
            image = await generateImage(message, data, state)
            return image, None
        except Exception as e:
            logger.error(f"Произошла ошибка при генерации изображения: {e}")
            return None, e

    # Создаем список задач
    tasks = [process_image(data) for _, data in enumerate(data_array)]
    
    # Запускаем все задачи параллельно
    await asyncio.gather(*tasks)

    return True

