from aiogram.fsm.context import FSMContext
from bot.settings import MOCK_MODE
from logger import logger

from bot.helpers.generateImages.dataArray import getSettingNumberByModelName
from bot.helpers.generateImages.process_image_block import process_image_block
from bot.helpers.jobs.get_job_ID import get_job_ID
from bot.helpers.generateImages.dataArray import getDataByModelName


# Функция для генерации изображений по объекту данных
async def generateImageBlock(
    model_name: str,
    message_id: int,
    state: FSMContext,
    user_id: int,
    setting_number: str,
    variable_prompt: str,
    is_test_generation: bool = False,
    checkOtherJobs: bool = True,
    chat_id: int = None,
):
    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    # Прибавляем к постоянному промпту переменный промпт
    json = data["json"].copy()
    json["input"]["prompt"] = variable_prompt.replace("\n", " ") + " " + json["input"]["prompt"]

    if not MOCK_MODE:
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
