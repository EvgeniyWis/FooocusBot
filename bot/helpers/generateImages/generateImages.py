import asyncio
import traceback
from typing import Any

from aiogram import types
from aiogram.fsm.context import FSMContext
from logger import logger

from bot.helpers.generateImages.dataArray import (
    getDataArrayByRandomizer,
    getDataArrayBySettingNumber,
    getDataByModelName,
    getModelNameByIndex,
)


async def generateImages(
    setting_number: int | str,
    prompt_for_current_model: dict[str, Any],
    message: types.Message,
    state: FSMContext,
    user_id: int,
    is_test_generation: bool,
    with_randomizer: bool = False,
    model_indexes_for_generation: list[int] = None,
):
    from bot.helpers.generateImages.generateImageBlock import (
        generateImageBlock,
    )

    state_data = await state.get_data()
    image_number = 10 if state_data.get("multi_select_mode") else 4

    # Получаем массив данных для генерации
    if not with_randomizer:
        if model_indexes_for_generation:
            model_names_for_generation = [
                getModelNameByIndex(model_index)
                for model_index in model_indexes_for_generation
            ]
            dataArray = [
                await getDataByModelName(model_name)
                for model_name in model_names_for_generation
            ]
        else:
            dataArray = getDataArrayBySettingNumber(setting_number)
    else:
        dataArray = await getDataArrayByRandomizer(state, setting_number)

    logger.info(
        f"Генерация изображений с помощью API для настройки {setting_number}. Длина массива: {len(dataArray)}. Переменный промпт: {prompt_for_current_model}",
    )

    await state.update_data(jobs={}, total_jobs_count=len(dataArray))
    images = []

    # Создаем карту model_name -> prompt из prompt_for_current_model
    name_to_prompt = {}
    if prompt_for_current_model:
        for index_str, prompt in prompt_for_current_model.items():
            try:
                model_name = getModelNameByIndex(int(index_str))
                if model_name:
                    name_to_prompt[model_name] = prompt
            except Exception:
                continue

    async def process_image(data: dict):
        try:
            if "json" in data and "input" in data["json"]:
                data["json"]["input"]["image_number"] = image_number

            model_name = data.get("model_name")
            prompt_for_model = name_to_prompt.get(model_name)

            image = await generateImageBlock(
                data,
                message.message_id,
                state,
                user_id,
                setting_number,
                prompt_for_model,
                is_test_generation,
                chat_id=message.chat.id,
            )
            images.append(image)
            return image, None
        except Exception as e:
            traceback.print_exc()
            raise Exception(f"Ошибка при генерации изображения: {e}")

    tasks = [asyncio.create_task(process_image(data)) for data in dataArray]
    results = await asyncio.gather(*tasks)
    images = [result[0] for result in results]
    return images
