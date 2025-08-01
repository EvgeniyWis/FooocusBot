import asyncio
import traceback
from typing import Any

from aiogram import types
from aiogram.fsm.context import FSMContext
from logger import logger

from bot.helpers.generateImages.dataArray.get_data_array_by_group_number import (
    get_data_array_by_group_number,
)
from bot.helpers.generateImages.dataArray.getDataArrayByRandomizer import (
    getDataArrayByRandomizer,
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
            dataArrayBase = get_data_array_by_group_number(setting_number)
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
        total_jobs_count=len(model_indexes_for_generation) if len(model_indexes_for_generation) > 0 else len(dataArrayBase),
    )
    images = []

    async def process_image(key: str):
        try:
            logger.info(f"Генерация изображения для модели {key}")
            base_index = int(key.split("+")[0])

            if len(base_model_indexes) > 0:
                try:
                    pos = base_model_indexes.index(base_index)
                except ValueError:
                    raise Exception(f"Модель с индексом {base_index} не найдена")
            else:
                pos = int(base_index) - 1

            data = dataArrayBase[pos]

            prompt_for_model = prompt_for_current_model.get(key, "")

            logger.info(f"Генерация изображения для модели {data['model_name']} с промптом {prompt_for_model}")

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
            raise e

    tasks = []

    # Если индексы не переданы, то получаем их из массива данных
    if not model_indexes_for_generation:
        model_indexes_for_generation = [str(index) for index, _ in enumerate(dataArrayBase)]

    for key in model_indexes_for_generation:
        state_data = await state.get_data()

        if state_data.get("stop_generation", False):
            logger.info("Генерация остановлена пользователем")
            break

        logger.info(f"Создание задачи для генерации изображения для модели {key}")
        tasks.append(asyncio.create_task(process_image(key)))
        await asyncio.sleep(0.1)

    results = await asyncio.gather(*tasks)
    images = [res[0] for res in results]
    return images
