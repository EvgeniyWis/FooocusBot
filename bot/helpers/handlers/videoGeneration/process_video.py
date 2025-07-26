from typing import Optional

from adapters.redis_task_storage_repository import key_for_video
from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.domain.entities.task import TaskProcessVideoDTO
from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    getModelNameIndex,
)
from bot.helpers.handlers.messages import send_progress_message
from bot.helpers.handlers.videoGeneration.check_video_path import (
    check_video_path,
)
from bot.InstanceBot import bot
from bot.keyboards import video_generation_keyboards
from bot.logger import logger
from bot.settings import settings
from bot.storage import get_redis_storage
from bot.utils.handlers import (
    appendDataToStateArray,
    deleteDataFromStateArray,
)


async def process_video(
    state: FSMContext,
    model_name: str,
    prompt: str,
    image_url: str | None = None,
    image_path: str | None = None,
    image_index: int | None = None,
    call: Optional[types.CallbackQuery] = None,
    message: Optional[types.Message] = None,
):
    """
    Обработка видео после генерации в основной рабочей генерации.
    Включает в себя работу с сообщениями, сохранением в стейт, генерацией и отправкой видео юзеру.

    Args:
        call: CallbackQuery - CallbackQuery с сообщением о генерации видео
        state: FSMContext - Контекст состояния
        model_name: str - Название модели для генерации видео
        prompt: str - Промпт для генерации видео
        image_url: str - Ссылка на изображение, из которого будет генерироваться видео
        image_path: str | None - Путь к изображению, из которого будет генерироваться видео
        image_index: int | None - Индекс изображения в массиве изображений
        call: Optional[types.CallbackQuery] = None - CallbackQuery с сообщением о генерации видео
        message: Optional[types.Message] = None - Message с сообщением о генерации видео
    """

    if (call is None and message is None) or (
        call is not None and message is not None
    ):
        raise ValueError(
            "Нужно передать либо call, либо message, но не оба и не ни одного."
        )

    if call is not None:
        user_id = call.from_user.id
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        callback_data = call.data
        message = call.message
    else:
        user_id = message.from_user.id
        chat_id = message.chat.id
        message_id = message.message_id
        callback_data = "generations_type|work"

    # Добавляем задачу в Redis для дальнейшего восстановления при перезапуске бота
    redis_storage = get_redis_storage()
    task_dto = TaskProcessVideoDTO(
        user_id=user_id,
        chat_id=chat_id,
        message_id=message_id,
        callback_data=callback_data,
        model_name=model_name,
        prompt=prompt,
        image_url=image_url,
        image_path=image_path,
    )
    await redis_storage.add_task(settings.PROCESS_VIDEO_TASK, task_dto)

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    video_progress_message_id = await send_progress_message(
        state,
        "video_generation_progress_messages",
        model_name,
        message,
        text.GENERATE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index),
        image_index,
    )

    # Проверяем путь к видео
    video_path = await check_video_path(
        prompt=prompt,
        message=message,
        image_index=image_index,
        image_url=image_url,
        temp_path=image_path,
        model_name=model_name,
    )

    # Удаляем сообщение о генерации видео
    try:
        await bot.delete_message(
            message.chat.id,
            video_progress_message_id,
        )
    except Exception as e:
        logger.error(f"Ошибка при удалении сообщения о генерации видео: {e}")

    # Удаляем из стейта данные о прогрессе генерации видео
    await deleteDataFromStateArray(
        state,
        "video_generation_progress_messages",
        model_name,
        "model_name",
    )

    if not video_path:
        data_for_update = {
            "model_name": model_name,
            "image_index": image_index,
        }
        await appendDataToStateArray(
            state,
            "video_generation_errors",
            data_for_update,
        )
        return

    # Добавляем путь к видео в стейт
    if image_index:
        data_for_update = {
            "image_index": image_index,
            "model_name": model_name,
            "direct_url": video_path,
        }
        await appendDataToStateArray(
            state,
            "generated_video_paths",
            data_for_update,
            unique_keys=("model_name", "image_index"),
        )
    else:
        data_for_update = {f"{model_name}": video_path}
        await appendDataToStateArray(
            state,
            "generated_video_paths",
            data_for_update,
        )

    # Отправляем видео юзеру
    video = types.FSInputFile(video_path)

    method = message.answer_video(
        video=video,
        caption=text.GENERATE_VIDEO_SUCCESS_TEXT.format(
            model_name,
            model_name_index,
        ),
        reply_markup=video_generation_keyboards.videoCorrectnessKeyboard(
            model_name,
            image_index,
        ),
    )
    video_message = await bot(method)

    # Сохраняем сообщение в стейт для последующего удаления
    if image_index:
        data_for_update = {
            "model_name": model_name,
            "image_index": image_index,
            "message_id": video_message.message_id,
        }
        await appendDataToStateArray(
            state,
            "videoGeneration_messages_ids",
            data_for_update,
            unique_keys=("model_name", "image_index"),
        )

    redis_storage = get_redis_storage()
    await redis_storage.delete_task(
        settings.PROCESS_VIDEO_TASK,
        key_for_video(
            "work",
            user_id=user_id,
            image_url=image_url if image_url else image_path,
            model_name=model_name,
        ),
    )
