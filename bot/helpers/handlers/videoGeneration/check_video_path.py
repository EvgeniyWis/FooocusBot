import traceback

from aiogram import types

from bot.helpers.generateImages.dataArray import getModelNameIndex
from bot.keyboards import video_generation_keyboards
from bot.logger import logger
from bot.settings import settings
from bot.utils import retryOperation, text
from bot.utils.handlers.messages import safe_send_message
from bot.utils.videos.generate_video import generate_video
from bot import constants


async def send_error_message(message: types.Message, image_index: int | None, model_name: str, e: str):
    """
    Отправляет сообщение об ошибке в зависимости от того, есть модель или нет

    Args:
        message: types.Message - сообщение с которым связан процесс генерации видео
        model_name: str - название модели
        e: str - текст ошибки

    Returns:
        None
    """

    model_name_index = getModelNameIndex(model_name) if model_name else None

    if model_name:
        await safe_send_message(
            text.GENERATE_VIDEO_ERROR_TEXT.format(
                model_name,
                model_name_index,
                e,
            ),
            message,
            reply_markup=video_generation_keyboards.videoGenerationTypeKeyboard(
                model_name,
                image_index,
                False,
                True
            ),
        )
    else:
        await safe_send_message(
            text.GENERATE_VIDEO_ERROR_TEXT_WITHOUT_MODEL.format(
                e,
            ),
            message,
        )


async def check_video_path(
    prompt: str,
    message: types.Message,
    image_index: int | None,
    image_url: str | None,
    temp_path: str | None,
    model_name: str = None,
) -> str | None:
    """
    Проверяет путь к видео на наличие ошибок и возвращает его в случае успеха.
    Если же ошибка, то отправляет сообщение об ошибке и возвращает None.

    Args:
        prompt: str - промпт для генерации видео
        image_index: int | None - индекс изображения в массиве изображений
        image_url: str - ссылка на изображение
        message: types.Message - сообщение с которым связан процесс генерации видео
        model_name: str - название модели

    Returns:
        str - путь к видео
        None - если ошибка
    """

    # Генерируем видео
    video_path = None
    if settings.MOCK_VIDEO_MODE:
        video_path = constants.MOCK_VIDEO_PATH
    else:
        try:
            video_path = await retryOperation(
                generate_video,
                10,
                1.5,
                prompt,
                image_url,
                temp_path,
            )
        except Exception as e:
            # Отправляем сообщение об ошибке
            traceback.print_exc()
            logger.error(f"Произошла ошибка при генерации видео: {e}")
            await send_error_message(message, image_index, model_name, e)

    if not video_path:
        await send_error_message(
            message, image_index, model_name, "Не удалось сгенерировать видео"
        )

    if isinstance(video_path, dict):
        error = video_path.get("error")
        if error:
            await send_error_message(message, image_index, model_name, error)

    return video_path
