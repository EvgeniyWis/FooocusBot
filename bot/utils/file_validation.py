import base64
import os
from typing import Tuple

from PIL import Image
from bot.app.core.logging import logger


class FileValidationError(Exception):
    """Исключение для ошибок валидации файлов"""
    pass


def validate_image_file(file_path: str) -> Tuple[int, int]:
    """
    Валидирует файл изображения.
    
    Args:
        file_path (str): Путь к файлу изображения
        
    Returns:
        Tuple[int, int]: Размеры изображения (width, height)
        
    Raises:
        FileValidationError: Если файл не прошел валидацию
    """
    try:
        # Проверяем размер файла
        file_size = os.path.getsize(file_path)
        logger.info(f"Размер файла: {file_size} байт")
        
        # Максимальный размер для API (обычно 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            raise FileValidationError(f"Файл слишком большой: {file_size} байт. Максимальный размер: {max_size} байт")
        
        # Проверяем, что файл существует и не пустой
        if not os.path.exists(file_path):
            raise FileValidationError(f"Файл не найден: {file_path}")
        
        if file_size == 0:
            raise FileValidationError("Файл пустой")
        
        # Проверяем формат файла (должен быть изображением)
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                logger.info(f"Размеры изображения: {width}x{height}")
                
                # Проверяем минимальные размеры
                if width < 100 or height < 100:
                    raise FileValidationError(f"Изображение слишком маленькое: {width}x{height}. Минимум: 100x100")
                
                # Проверяем максимальные размеры
                if width > 4096 or height > 4096:
                    raise FileValidationError(f"Изображение слишком большое: {width}x{height}. Максимум: 4096x4096")
                
                # Проверяем формат
                if img.format not in ['JPEG', 'PNG', 'WEBP']:
                    raise FileValidationError(f"Неподдерживаемый формат изображения: {img.format}")
                
                return width, height
                    
        except Exception as e:
            raise FileValidationError(f"Ошибка при проверке изображения: {e}")
            
    except FileValidationError:
        raise
    except Exception as e:
        raise FileValidationError(f"Неожиданная ошибка при валидации файла: {e}")


def validate_base64_string(base64_str: str) -> int:
    """
    Валидирует base64 строку.
    
    Args:
        base64_str (str): Base64 строка для валидации
        
    Returns:
        int: Длина base64 строки
        
    Raises:
        FileValidationError: Если строка не прошла валидацию
    """
    try:
        # Проверяем, что base64 строка не пустая
        if not base64_str:
            raise FileValidationError("Base64 строка пустая")
        
        # Проверяем длину base64 строки
        if len(base64_str) > 50 * 1024 * 1024:  # 50MB в base64
            raise FileValidationError(f"Base64 строка слишком длинная: {len(base64_str)} символов")
        
        # Проверяем, что это валидная base64 строка
        try:
            base64.b64decode(base64_str)
        except Exception:
            raise FileValidationError("Некорректная base64 строка")
            
        logger.info(f"Base64 строка валидна, длина: {len(base64_str)} символов")
        return len(base64_str)
        
    except FileValidationError:
        raise
    except Exception as e:
        raise FileValidationError(f"Неожиданная ошибка при валидации base64: {e}")


def validate_image_for_magnific(file_path: str) -> Tuple[int, int, str]:
    """
    Комплексная валидация изображения для Magnific API.
    
    Args:
        file_path (str): Путь к файлу изображения
        
    Returns:
        Tuple[int, int, str]: (width, height, base64_string)
        
    Raises:
        FileValidationError: Если файл не прошел валидацию
    """
    # Валидируем файл
    width, height = validate_image_file(file_path)
    
    # Читаем содержимое файла и преобразуем в base64
    with open(file_path, 'rb') as image_file:
        image_bytes = image_file.read()
        base64_str = base64.b64encode(image_bytes).decode("utf-8")
    
    # Валидируем base64 строку
    validate_base64_string(base64_str)
    
    return width, height, base64_str 