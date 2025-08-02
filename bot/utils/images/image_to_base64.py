import base64
import io
import logging

from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)


def is_valid_image(image: Image.Image) -> bool:
    """
    Проверяет, является ли изображение валидным.
    
    Args:
        - image: PIL Image, изображение для проверки
        
    Returns:
        - bool: True если изображение валидно, False в противном случае
    """
    try:
        # Проверяем, что изображение имеет режим
        if not image.mode:
            return False
            
        # Пытаемся загрузить изображение
        image.load()
        
        # Проверяем размеры изображения
        if image.size[0] <= 0 or image.size[1] <= 0:
            return False
            
        return True
        
    except (OSError, UnidentifiedImageError, ValueError):
        return False


def image_to_base64(image: Image.Image) -> str:
    """
    Преобразует изображение в base64.

    Args:
        - image: PIL Image, изображение для преобразования

    Returns:
        - base64_image: строка base64, содержащая изображение
        
    Raises:
        - ValueError: если изображение повреждено или не может быть обработано
    """
    try:
        # Проверяем валидность изображения
        if not is_valid_image(image):
            raise ValueError("Изображение повреждено или имеет недопустимый формат")
        
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
        
    except Exception as e:
        logger.error(f"Ошибка при преобразовании изображения в base64: {e}")
        raise ValueError(f"Не удалось преобразовать изображение в base64: {e}")
