import base64

from aiogram.fsm.context import FSMContext

from bot.factory.image_service_factory import create_image_upscaler
from bot.logger import logger
from bot.utils.handlers import appendDataToStateArray
from bot.utils.images import base64_to_image


async def second_upscale_image(
    temp_image_path: str,
    model_name: str,
    image_index: int,
    user_id: int,
    state: FSMContext,
):
    """
    Функция для второго upscale изображения с помощью ILoveAPI

    Args:
        temp_image_path (str): путь к временному изображению
        model_name (str): название модели
        image_index (int): индекс изображения
        user_id (int): айди пользователя
        state (FSMContext): контекст состояния

    Returns:
        str: путь к изображению
    """
    # Получаем сервис ILoveAPI для увеличения качества изображения
    upscale_service = create_image_upscaler()

    # Запускаем задачу
    try:
        upscale_result_response = await upscale_service.upscale_image_file(
            file=temp_image_path,
            multiplier=2,
        )
        upscale_result = upscale_result_response.content

        # ArrayBuffer to base64
        image_data = base64.b64encode(upscale_result).decode("utf-8")

        # Сохраняем изображения по этому же пути
        return await base64_to_image(
            image_data,
            model_name,
            image_index,
            user_id,
            False,
        )
    except Exception as e:
        error_text = f"Ошибка при увеличении качества изображения: {e}"
        logger.error(error_text)
        data_for_update = {
            "model_name": model_name,
            "image_index": image_index,
        }
        await appendDataToStateArray(
            state,
            "second_upscale_errors",
            data_for_update,
        )
        raise e