import asyncio
import traceback

from aiogram import types
from aiogram.fsm.context import FSMContext
from logger import logger

from .dataArray import getDataArrayByRandomizer, getDataArrayWithRootPrompt
from .generateImageBlock import generateImageBlock


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
        # Прибавляем к каждому элементу массива корневой промпт
        if model_indexes_for_generation:
            dataArray = await getDataArrayWithRootPrompt(setting_number, prompt, model_indexes_for_generation)
        else:
            dataArray = await getDataArrayWithRootPrompt(setting_number, prompt)
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

            # Прибавляем к каждому элементу массива корневой промпт
            json = data["json"].copy()
            json["input"]["prompt"] += " " + prompt

            image = await generateImageBlock(
                json,
                data["model_name"],
                message,
                state,
                user_id,
                setting_number,
                is_test_generation,
            )
            images.append(image)
            return image, None
        except Exception as e:
            traceback.print_exc()
            raise Exception(f"Произошла ошибка при генерации изображения во внутренней функции: {e}")

    # Создаем список задач, выполняющихся параллельно
    tasks = [asyncio.create_task(process_image(data)) for data in dataArray]

    # Ждем выполнения всех задач
    results = await asyncio.gather(*tasks)
    images = [result[0] for result in results]

    return images
