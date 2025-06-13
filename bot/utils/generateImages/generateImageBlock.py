from aiogram import types
from aiogram.fsm.context import FSMContext
from config import MOCK_MODE

from logger import logger

from utils.jobs.get_job_ID import get_job_ID
from utils.generateImages.dataArray import getSettingNumberByModelName

from utils.generateImages.process_image_block import process_image_block
from RunBot import redis_task_storage



# Функция для генерации изображений по объекту данных
async def generateImageBlock(
    dataJSON: dict,
    model_name: str,
    message_id: int,
    state: FSMContext,
    user_id: int,
    setting_number: str,
    is_test_generation: bool = False,
    checkOtherJobs: bool = True,
    chat_id: int = None,
):
    if not MOCK_MODE:
        # Получаем номер настройки по имени модели
        setting_number = getSettingNumberByModelName(model_name)

        # Логируем наш json
        logger.info(f"Отправляем запрос на генерацию изображений с данными: {dataJSON}")

        # Делаем запрос на генерацию и получаем id работы
        job_id = await get_job_ID(dataJSON, setting_number, state, user_id, "image_generation")

        # Обрабатываем работу
        result = await process_image_block(job_id, model_name, setting_number, user_id, 
        state, message_id, is_test_generation, checkOtherJobs, task_repo=redis_task_storage, chat_id=chat_id)

        return result