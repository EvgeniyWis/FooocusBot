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
    model_indexes_for_generation: list[str] = None,
):
    from bot.helpers.generateImages.generateImageBlock import (
        generateImageBlock,
    )

    base_model_indexes = (
        [int(idx.split("+")[0]) for idx in model_indexes_for_generation]
        if model_indexes_for_generation
        else []
    )

    if not with_randomizer:
        if base_model_indexes:
            dataArrayBase = await get_data_array_by_model_indexes(
                base_model_indexes,
            )
        else:
            dataArrayBase = getDataArrayBySettingNumber(setting_number)
    else:
        dataArrayBase = await getDataArrayByRandomizer(
            state,
            setting_number,
            base_model_indexes,
        )

    logger.info(
        f"Генерация изображений с помощью API для настройки {setting_number}. Длина массива: {len(model_indexes_for_generation)}. Переменный промпт: {prompt_for_current_model}",
    )

    await state.update_data(
        jobs={},
        total_jobs_count=len(model_indexes_for_generation),
    )
    images = []

    async def process_image(key: str):
        try:
            base_index = int(key.split("+")[0])
            try:
                pos = base_model_indexes.index(base_index)
            except ValueError:
                raise Exception(f"Модель с индексом {base_index} не найдена")

            data = dataArrayBase[pos]

            prompt_for_model = prompt_for_current_model.get(key, "")

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
        except Exception:
            traceback.print_exc()
            raise

    tasks = []
    for key in model_indexes_for_generation:
        state_data = await state.get_data()
        if state_data.get("stop_generation", False):
            break
        tasks.append(asyncio.create_task(process_image(key)))
        await asyncio.sleep(0.1)

    results = await asyncio.gather(*tasks)
    images = [res[0] for res in results]
    return images
