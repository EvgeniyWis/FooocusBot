import os
from typing import Any

from bot.logger import logger

from ..client.api_client import ILoveApiClient
from ..services.task_service import ILoveApiTaskService
from ..utils.retry import download_with_retry


class ILoveApiUpscaler:
    """Сервис для апскейла изображений через ILoveAPI"""
    
    def __init__(self):
        self.client = ILoveApiClient()
        self.task_service = ILoveApiTaskService(self.client)
    
    async def process_upscale_task(self, temp_image_path: str, multiplier: int) -> Any:
        """
        Внутренняя функция для обработки задачи upscale с повторными попытками
        """
        # Проверяем существование файла
        if not os.path.exists(temp_image_path):
            raise FileNotFoundError(f"Файл для upscale не найден: {temp_image_path}")
        
        # Проверяем размер файла
        file_size = os.path.getsize(temp_image_path)
        if file_size == 0:
            raise ValueError(f"Файл пустой: {temp_image_path}")
        
        logger.info(f"Создаю задачу upscaleimage для файла размером {file_size} байт")
        
        try:
            # Обрабатываем задачу с повторными попытками
            task = self.task_service.process_task_with_retry(temp_image_path, "upscaleimage", multiplier=multiplier)
            
            # Скачиваем результат с повторными попытками
            if download_with_retry(task, temp_image_path, self.client, self.task_service):
                logger.info("Задача успешно выполнена!")
            else:
                raise Exception("Не удалось скачать файл ни одним способом")
            
        except Exception as e:
            logger.error(f"Критическая ошибка при обработке upscale: {e}")
            raise
        
        # Проверяем, что файл был обновлен
        if not os.path.exists(temp_image_path):
            raise FileNotFoundError(f"Обработанный файл не найден после загрузки: {temp_image_path}")
        
        new_file_size = os.path.getsize(temp_image_path)
        logger.info(f"Файл успешно обработан. Новый размер: {new_file_size} байт")
        
        return task
