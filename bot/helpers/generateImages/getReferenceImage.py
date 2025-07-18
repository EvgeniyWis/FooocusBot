import os

import aiofiles

from bot.helpers.generateImages.dataArray.getModelNameIndex import (
    getModelNameIndex,
)
from bot.logger import logger


# Функция для получения референсного изображения
async def getReferenceImage(model_name: str, user_id: int) -> str:
    # Получаем индекс модели
    model_index = await getModelNameIndex(model_name, user_id)

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
