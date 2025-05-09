from utils.generateImages.data_array.getDataArrayWithRootPrompt import getDataArrayWithRootPrompt
from utils.generateImages.generateImage import generateImage
from logger import logger
from aiogram import types
import asyncio
from aiogram.fsm.context import FSMContext


# Функция для генерации изображений с помощью API
async def generateImages(prompt: str, message: types.Message, state: FSMContext, folder_name: str, user_id: int):
    # Прибавляем к каждому элементу массива корневой промпт
    dataArray = getDataArrayWithRootPrompt(prompt)

    # Генерируем изображения по всем элементам массива
    jobs = {}
    await state.update_data(jobs=jobs)

    # Инициализируем папку для хранения изображений
    images = []

    async def process_image(index, data):
        try:
            logger.info(f"Генерация изображения с изначальным промптом: {data['input']['prompt']}")
            image = await generateImage(message, data, state, folder_name, index, user_id)
            images.append(image)
            return image, None
        except Exception as e:
            logger.error(f"Произошла ошибка при генерации изображения во внутренней функции: {e}")
            return None, e

    # Создаем список задач
    tasks = [process_image(index, data) for index, data in enumerate(dataArray)]
    
    # Запускаем все задачи параллельно
    await asyncio.gather(*tasks)

    return images

