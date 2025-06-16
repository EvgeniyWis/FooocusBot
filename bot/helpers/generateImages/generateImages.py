import asyncio
import traceback

from aiogram import types
from aiogram.fsm.context import FSMContext
from logger import logger

from bot.helpers.generateImages.dataArray import (
    getDataArrayByRandomizer,
    getDataArrayBySettingNumber,
    getDataByModelName,
    getModelNameByIndex,
)
from bot.helpers.generateImages.generateImageBlock import generateImageBlock


# Функция для генерации изображений с помощью API
async def generateImages(
    setting_number: int | str,
    prompt: str,
    message: types.Message,
    state: FSMContext,
    user_id: int,
    is_test_generation: bool,
    with_randomizer: bool = False,
    model_indexes_for_generation: list[int] = None,
):
    if not with_randomizer:
        # Если модели для индивидуальной генерации есть, то формируем из них массив
        if model_indexes_for_generation:
            # Получаем имена моделей по их номерам
            model_names_for_generation = [
                getModelNameByIndex(model_index)
                for model_index in model_indexes_for_generation
            ]
            dataArray = [
                await getDataByModelName(model_name)
                for model_name in model_names_for_generation
            ]
        else:
            dataArray = getDataArrayBySettingNumber(int(setting_number))
    else:
        dataArray = await getDataArrayByRandomizer(state, setting_number)

    logger.info(
        f"Генерация изображений с помощью API для настройки {setting_number}. Длина массива: {len(dataArray)}",
    )

    # Обновляем стейт
    jobs = {}
    await state.update_data(jobs=jobs)
    await state.update_data(total_jobs_count=len(dataArray))

    # Инициализируем папку для хранения изображений
    images = []

    async def process_image(data: tuple[dict, str, str]):
        try:
            logger.info(
                f"Генерация изображения с изначальными данными: {data}",
            )

            image = await generateImageBlock(
                data,
                message.message_id,
                state,
                user_id,
                setting_number,
                prompt,
                is_test_generation,
                chat_id=message.chat.id,
            )
            images.append(image)
            return image, None
        except Exception as e:
            traceback.print_exc()
            raise Exception(
                f"Произошла ошибка при генерации изображения во внутренней функции: {e}"
            )

    # Создаем список задач, выполняющихся параллельно
    tasks = [asyncio.create_task(process_image(data)) for data in dataArray]

    # Ждем выполнения всех задач
    results = await asyncio.gather(*tasks)
    images = [result[0] for result in results]

    return images
