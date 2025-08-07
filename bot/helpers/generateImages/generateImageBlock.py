import copy

from aiogram.fsm.context import FSMContext
from logger import logger

from bot.helpers.generateImages.dataArray import (
    get_setting_number_by_model_name,
)
from bot.helpers.jobs.get_job_ID import get_job_ID


# Функция для генерации изображений по объекту данных
async def generateImageBlock(
    data: dict,
    message_id: int,
    state: FSMContext,
    user_id: int,
    variable_prompt: str,
    checkOtherJobs: bool = True,
    chat_id: int = None,
    model_key: str = None,
):
    # Проверяем наличие переменного промпта
    if not variable_prompt:
        variable_prompt = " "

    # Проверяем наличие json в данных модели
    if "json" not in data:
        raise ValueError(f"Не получилось обнаружить json в {data}")

    # Прибавляем к постоянному промпту переменный промпт
    json = copy.deepcopy(data["json"])
    json["input"]["prompt"] = (
        variable_prompt.replace("\n", " ") + " " + json["input"]["prompt"]
    )
    json["input"]["prompt"] = json["input"]["prompt"].lstrip(" ")

    # Получаем имя модели
    model_name = data["model_name"]

    # Логируем наш json
    logger.info(
        f"Отправляем запрос на генерацию изображений с данными: {json}",
    )

    # Получаем номер настройки по имени модели
    setting_number = get_setting_number_by_model_name(model_name)

    # Делаем запрос на генерацию и получаем id работы
    job_id = await get_job_ID(
        json,
        setting_number,
        state,
        user_id,
        "image_generation",
    )
    state_data = await state.get_data()
    job_map = state_data.get("job_id_to_full_model_key", {})
    
    # Формируем полный ключ модели
    if model_key:
        full_model_key = f"{model_name}_{model_key}"
    else:
        # Обратная совместимость - используем старый формат
        full_model_key = f"{model_name}_{setting_number}"
    
    job_map[job_id] = full_model_key
    await state.update_data(job_id_to_full_model_key=job_map)

    logger.info(
        f"[generateImageBlock] Сохранили: {job_id} -> {full_model_key}",
    )

    # Обрабатываем работу
    from helpers.generateImages.process_image_block import (
        process_image_block,
    )

    result = await process_image_block(
        job_id,
        model_name,
        user_id,
        state,
        message_id,
        checkOtherJobs,
        chat_id=chat_id,
        model_key=model_key,
    )

    return result, job_id
