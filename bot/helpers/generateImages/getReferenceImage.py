import os

import aiofiles

from bot.logger import logger

from bot.helpers.generateImages.dataArray import get_model_index_by_model_name


# Функция для получения референсного изображения
async def getReferenceImage(model_name: str) -> str:
    # Получаем индекс модели
    model_index = get_model_index_by_model_name(model_name)

    reference_image_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "assets",
            "reference_images",
            f"{model_index}. {model_name}.jpg",
        ),
    )

    # Асинхронная проверка на существование файла
    try:
        async with aiofiles.open(
            reference_image_path,
        ) as _:  # Проверка существования
            pass
    except FileNotFoundError:
        logger.error(
            f"Файл с референсным изображением для модели {model_name} по пути {reference_image_path} не найден.",
        )
        return ""

    logger.info(
        f"Получено референсное изображение для модели {model_name}: {reference_image_path}.",
    )
    return reference_image_path
