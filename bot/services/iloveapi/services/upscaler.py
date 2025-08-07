from typing import Any

from bot.logger import logger
from bot.services.iloveapi.client.api_client import ILoveApiClient
from bot.services.iloveapi.services.task_service import ILoveApiTaskService
from bot.services.iloveapi.utils.file_validator import APIFileValidator
from bot.services.iloveapi.utils.retry import download_with_retry


class ILoveApiUpscaler:
    """Сервис для апскейла изображений через ILoveAPI"""
    
    def __init__(self):
        self.client = ILoveApiClient()
        self.task_service = ILoveApiTaskService(self.client)
        self.validator = APIFileValidator()
    
    async def process_upscale_task(self, temp_image_path: str, multiplier: int) -> Any:
        """
        Внутренняя функция для обработки задачи upscale с повторными попытками
        """
        try:
            # Валидируем исходный файл
            if not self.validator.validate_source_file(temp_image_path):
                raise Exception("Исходный файл не прошел валидацию")
            
            # Обрабатываем задачу с повторными попытками
            task = self.task_service.process_task_with_retry(temp_image_path, "upscaleimage", multiplier=multiplier)
            
            # Скачиваем результат с повторными попытками
            if download_with_retry(task, temp_image_path):
                logger.info("Задача успешно выполнена!")
                
                # Валидируем скачанный файл
                if not self.validator.validate_downloaded_file(temp_image_path):
                    raise Exception("Скачанный файл не прошел валидацию - возможно, API вернул поврежденный файл")
            else:
                raise Exception("Не удалось скачать файл ни одним способом")
            
        except Exception as e:
            logger.error(f"Критическая ошибка при обработке upscale: {e}")
            raise
        
        return task
