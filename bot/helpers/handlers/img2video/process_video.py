import traceback

from aiogram import types

from bot.helpers import text
from bot.helpers.generateImages.dataArray.getModelNameByIndex import (
    getModelNameByIndex,
)
from bot.helpers.handlers.videoGeneration import (
    check_video_path,
)
from bot.keyboards import video_generation_keyboards
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)


async def process_video(
    message: types.Message,
    prompt: str,
    image_index: int,
    model_index: int,
    temp_paths_for_video_generation: list[str],
) -> str:
    """
    Обрабатывает видео для одного изображения для одной модели (по её индексу).
    Присылает сообщение с прогрессом генерации видео. 
    После обработки присылает готовое видео с возможностью сохранения или перегенерации.

    Args:
        message (types.Message): Сообщение с изображением.
        prompt (str): Промпт для генерации видео.
        image_index (int): Индекс изображения.
        model_index (int): Индекс модели.
        temp_paths_for_video_generation (list[str]): Список путей к временным файлам 
        (отправленных пользователем изображениям) для генерации видео.

    Returns:
        str: Путь к сгенерированному видео.
    """
    model_name = getModelNameByIndex(model_index)
    generate_video_from_image_progress_message = await safe_send_message(
        text.GENERATE_VIDEO_PROGRESS_TEXT.format(model_name, model_index),
        message,
    )
    try:
        video_path = await check_video_path(
            prompt,
            message,
            image_index=None,
            image_url=None,
            temp_path=temp_paths_for_video_generation[image_index - 1],
            model_name=None,
        )

        await generate_video_from_image_progress_message.delete()

        if not video_path:
            return

        video = types.FSInputFile(video_path)
        await message.answer_video(
            video=video,
            caption=text.GENERATE_VIDEO_SUCCESS_TEXT.format(model_name, model_index),
            reply_markup=video_generation_keyboards.videoCorrectnessKeyboard(
                model_name,
                image_index=None,
            ),
        )

        return model_name, video_path
    except Exception as e:
        traceback.print_exc()
        raise e