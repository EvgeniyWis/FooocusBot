
from utils.jobs.checkJobStatus import checkJobStatus
from aiogram.fsm.context import FSMContext

from aiogram.fsm.context import FSMContext

from utils.generateImages import base64ToImage



async def check_upscale_status(job_id: str, setting_number: int, state: FSMContext,
    model_name: str, image_index: int, user_id: int, message_id: int) -> str:
    """
    Функция для проверки статуса работы upscale и отсылания улучшенного изображения

    Attributes:
        job_id (str): id работы
        setting_number (int): номер настройки
        state (FSMContext): контекст состояния
        model_name (str): название модели
        image_index (int): индекс изображения
        user_id (int): id пользователя
    """

    # Проверяем статус работы
    response_json = await checkJobStatus(job_id, setting_number, user_id, message_id, state, 
    timeout=1000, checkOtherJobs=False)

    if not response_json:
        raise Exception("Не удалось сделать upscale для изображения")

    # Получаем изображение
    image_data = response_json["output"][0]["base64"]
    
    # Сохраняем изображения по этому же пути
    return await base64ToImage(
        image_data,
        model_name,
        int(image_index) - 1,
        user_id,
        False)