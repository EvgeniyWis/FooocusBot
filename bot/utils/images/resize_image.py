from PIL import Image

from bot.app.core.logging import logger


async def resize_image(image_path: str, target_width: int, target_height: int) -> str:
    """
    Локально изменяет размер изображения с помощью Pillow
    
    Args:
        image_path: Путь к исходному изображению
        target_width: Целевая ширина
        target_height: Целевая высота
    
    Returns:
        str: Путь к измененному изображению (тот же файл)
    
    Raises:
        Exception: Если не удалось изменить размер изображения
    """
    try:
        logger.info(f"Изменяю размер изображения {image_path} до {target_width}x{target_height}")
        
        # Открываем изображение
        with Image.open(image_path) as img:
            # Изменяем размер с сохранением пропорций
            resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Сохраняем обратно в тот же файл
            resized_img.save(image_path, quality=100, optimize=True)
            
        logger.info(f"Размер изображения успешно изменен: {image_path}")
        return image_path
        
    except Exception as e:
        error_msg = f"Ошибка при изменении размера изображения {image_path}: {e}"
        logger.error(error_msg)
        raise Exception(error_msg) 