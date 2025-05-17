import os
from logger import logger


# Функция для получения референсного изображения
async def getReferenceImage(model_name: str) -> str:
    # Обращаемся по пути assets/reference_images/model_name.png (поднимаемся на два уровня вверх)
    reference_image_path = os.path.abspath(f"FocuuusBot/bot/assets/reference_images/{model_name}.jpeg")

    logger.info(f"Получено референсное изображение для модели {model_name}: {reference_image_path}")
    
    return reference_image_path

