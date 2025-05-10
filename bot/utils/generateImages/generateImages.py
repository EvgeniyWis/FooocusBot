from utils.generateImages.dataArray.getDataArrayWithRootPrompt import getDataArrayWithRootPrompt
from utils.generateImages.generateImage import generateImage
from logger import logger
from aiogram import types
import asyncio
from aiogram.fsm.context import FSMContext


# Функция для генерации изображений с помощью API
async def generateImages(setting_number: int, prompt: str, message: types.Message, state: FSMContext, 
    user_id: int, is_test_generation: bool):
    # Прибавляем к каждому элементу массива корневой промпт
    dataArray = getDataArrayWithRootPrompt(setting_number, prompt)

    # Генерируем изображения по всем элементам массива
    jobs = {}
    await state.update_data(jobs=jobs)

    # Инициализируем папку для хранения изображений
    images = []

    async def process_image(data):
        try:
            logger.info(f"Генерация изображения с изначальным промптом: {data['input']['prompt']}")
            image = await generateImage(message, data, state, user_id, is_test_generation)
            images.append(image)
            return image, None
        except Exception as e:
            logger.error(f"Произошла ошибка при генерации изображения во внутренней функции: {e}")
            return None, e

    # Создаем список задач
    tasks = [process_image(data) for data in dataArray]
    
    # Запускаем все задачи параллельно
    await asyncio.gather(*tasks)

    return images

