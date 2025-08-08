import os
from typing import Tuple

from PIL import Image

from bot.app.core.logging import logger


class APIFileValidator:
    """Валидатор файлов для API операций"""
    
    @staticmethod
    def validate_source_file(file_path: str) -> bool:
        """
        Валидирует исходный файл перед отправкой в API
        
        Args:
            file_path (str): Путь к файлу
            
        Returns:
            bool: True если файл валиден, False в противном случае
        """
        try:
            # Проверяем размер файла
            file_size = os.path.getsize(file_path)
            logger.info(f"Размер исходного файла: {file_size} байт")
            
            if file_size == 0:
                logger.error("Исходный файл пустой")
                return False
            
            # Проверяем, что это валидное изображение
            with Image.open(file_path) as img:
                width, height = img.size
                logger.info(f"Размеры исходного изображения: {width}x{height}")
                
                # Проверяем минимальные размеры
                if width < 10 or height < 10:
                    logger.error(f"Исходное изображение слишком маленькое: {width}x{height}")
                    return False
                
                # Проверяем формат
                if img.format not in ['JPEG', 'PNG', 'WEBP']:
                    logger.error(f"Неподдерживаемый формат исходного изображения: {img.format}")
                    return False
                
                logger.info("Исходный файл прошел валидацию")
                return True
                
        except Exception as e:
            logger.error(f"Ошибка при валидации исходного файла: {e}")
            return False
    
    @staticmethod
    def validate_downloaded_file(file_path: str) -> bool:
        """
        Валидирует скачанный файл после обработки API
        
        Args:
            file_path (str): Путь к файлу
            
        Returns:
            bool: True если файл валиден, False в противном случае
        """
        try:
            # Проверяем размер файла
            file_size = os.path.getsize(file_path)
            logger.info(f"Размер скачанного файла: {file_size} байт")
            
            if file_size == 0:
                logger.error("Скачанный файл пустой")
                return False
            
            # Проверяем, что это валидное изображение
            with Image.open(file_path) as img:
                width, height = img.size
                logger.info(f"Размеры скачанного изображения: {width}x{height}")
                
                # Проверяем минимальные размеры
                if width < 10 or height < 10:
                    logger.error(f"Скачанное изображение слишком маленькое: {width}x{height}")
                    return False
                
                # Проверяем формат
                if img.format not in ['JPEG', 'PNG', 'WEBP']:
                    logger.error(f"Неподдерживаемый формат скачанного изображения: {img.format}")
                    return False
                
                logger.info("Скачанный файл прошел валидацию")
                return True
                
        except Exception as e:
            logger.error(f"Ошибка при валидации скачанного файла: {e}")
            return False
    
    @staticmethod
    def get_file_info(file_path: str) -> Tuple[int, int, str]:
        """
        Получает информацию о файле
        
        Args:
            file_path (str): Путь к файлу
            
        Returns:
            Tuple[int, int, str]: (width, height, format)
        """
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                format_name = img.format or "Unknown"
                return width, height, format_name
        except Exception as e:
            logger.error(f"Ошибка при получении информации о файле: {e}")
            return 0, 0, "Error" 