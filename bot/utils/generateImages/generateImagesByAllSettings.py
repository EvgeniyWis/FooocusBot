from .dataArray.getAllDataArrays import getAllDataArrays
from logger import logger
from aiogram import types
from utils import text
from aiogram.fsm.context import FSMContext
import traceback
from .generateImage import generateImage
import asyncio

# Функция для генерации изображений по всем настройкам
async def generateImagesByAllSettings(message: types.Message, state: FSMContext, user_id: int,
    is_test_generation: bool):

    # Получаем все настройки
    dataArrays = getAllDataArrays()
    settings_numbers_success = []
    semaphore = asyncio.Semaphore(3)

    # Создаём сообщение с прогрессом генерации настроек
    message_with_settings = await message.answer(text.TEST_GENERATION_WITH_ALL_SETTINGS_PROGRESS_TEXT
    .format("❌", "❌", "❌", "❌"))

    # Создаём сообщение с прогрессом генерации изображений
    message_with_generations_status = await message.answer(text.GET_PROMPT_SUCCESS_TEXT)

    async def process_generation(dataJSON, model_name, index):
        async with semaphore:
            await generateImage(dataJSON, model_name, message_with_generations_status, state, user_id, index + 1, is_test_generation)

    try:
        for index, dataArray in enumerate(dataArrays):
            tasks = []
            if is_test_generation:
                dataJSON = dataArray[0]["json"]  
                model_name = dataArray[0]["model_name"]
                task = asyncio.create_task(process_generation(dataJSON, model_name, index))
                tasks.append(task)
            else:
                for data in dataArray:
                    # Получаем данные
                    model_name = data["model_name"]
                    dataJSON = data["json"]
                    
                    # Обновляем стейт
                    jobs = {}
                    await state.update_data(jobs=jobs)
                    await state.update_data(total_jobs_count=len(dataArray))

                    # Генерируем изображение
                    task = asyncio.create_task(process_generation(dataJSON, model_name, index))
                    tasks.append(task)

            await asyncio.gather(*tasks)
            settings_numbers_success.append(index)
            
            await message_with_settings.edit_text(text.TEST_GENERATION_WITH_ALL_SETTINGS_PROGRESS_TEXT
            .format("✅" if 0 in settings_numbers_success else "❌", 
            "✅" if 1 in settings_numbers_success else "❌", "✅" if 2 in settings_numbers_success else "❌", "✅" if 3 in settings_numbers_success else "❌"))

        return True
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Ошибка при тестовой генерации по всем настройкам: {e}")
        return False