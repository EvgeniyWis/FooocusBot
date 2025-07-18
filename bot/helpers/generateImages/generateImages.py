import asyncio
import traceback
from typing import Any

from aiogram import types
from aiogram.fsm.context import FSMContext
from logger import logger

from bot.helpers.generateImages.dataArray.getDataArrayByRandomizer import (
    getDataArrayByRandomizer,
)
from bot.helpers.generateImages.dataArray.getDataArrayBySettingNumber import (
    getDataArrayBySettingNumber,
)
from bot.helpers.generateImages.dataArray.getModelNameByIndex import (
    getModelNameByIndex,
)
from bot.helpers.generateImages.get_data_array_by_model_indexes import (
    get_data_array_by_model_indexes,
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

    # Получаем массив данных для генерации
    if not with_randomizer:
        if model_indexes_for_generation:
            dataArray = await get_data_array_by_model_indexes(model_indexes_for_generation)
        else:
            dataArray = getDataArrayBySettingNumber(setting_number)
    else:
        dataArray = await getDataArrayByRandomizer(state, setting_number, model_indexes_for_generation)

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
            raise Exception(e)

    tasks = []
    for data in dataArray:
        state_data = await state.get_data()
        stop_generation = state_data.get("stop_generation", False)

        if not stop_generation:
            tasks.append(asyncio.create_task(process_image(data)))
            await asyncio.sleep(0.1)  # Задержка в 0.1 секунду между созданием задач

    results = await asyncio.gather(*tasks)
    images = [result[0] for result in results]
    return images
