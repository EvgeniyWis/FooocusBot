from aiogram.fsm.context import FSMContext
from logger import logger

from bot.helpers.generateImages.dataArray import getSettingNumberByModelName
from bot.helpers.jobs.get_job_ID import get_job_ID
from bot.settings import settings

process_image_block = None


def set_process_image_block(module):
    global process_image_block
    from bot.helpers.generateImages.process_image_block import (
        process_image_block as pic,
    )

    process_image_block = pic


# Функция для генерации изображений по объекту данных
async def generateImageBlock(
    data: dict,
    message_id: int,
    state: FSMContext,
    user_id: int,
    setting_number: str,
    variable_prompt: str,
    is_test_generation: bool = False,
    checkOtherJobs: bool = True,
    chat_id: int = None,
):
    # Проверяем наличие переменного промпта
    if not variable_prompt:
        variable_prompt = " "

    # Прибавляем к постоянному промпту переменный промпт
    json = data["json"].copy()
    json["input"]["prompt"] = (
        variable_prompt.replace("\n", " ") + " " + json["input"]["prompt"]
    )

    # Получаем имя настройки
    model_name = data["model_name"]

    if not settings.MOCK_MODE:
        # Получаем номер настройки по имени модели
        setting_number = getSettingNumberByModelName(model_name)

        # Логируем наш json
        logger.info(
            f"Отправляем запрос на генерацию изображений с данными: {json}",
        )

        # Делаем запрос на генерацию и получаем id работы
        job_id = await get_job_ID(
            json,
            setting_number,
            state,
            user_id,
            "image_generation",
        )

        # Обрабатываем работу
        result = await process_image_block(
            job_id,
            model_name,
            setting_number,
            user_id,
            state,
            message_id,
            is_test_generation,
            checkOtherJobs,
            chat_id=chat_id,
        )

        return result
