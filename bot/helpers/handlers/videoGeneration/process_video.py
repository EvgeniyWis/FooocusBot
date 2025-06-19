import traceback

from adapters.redis_task_storage_repository import key_for_video
from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.domain.entities.task import TaskProcessVideoDTO
from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    getModelNameIndex,
)
from bot.InstanceBot import bot
from bot.keyboards import video_generation_keyboards
from bot.logger import logger
from bot.settings import settings
from bot.storage import get_redis_storage
from bot.utils import retryOperation
from bot.utils.handlers import (
    appendDataToStateArray,
)
from bot.utils.handlers.messages import (
    editMessageOrAnswer,
)
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)
from bot.utils.videos import generate_video


async def process_video(
    call: types.CallbackQuery,
    state: FSMContext,
    model_name: str,
    prompt: str,
    type_for_video_generation: str,
    image_url: str,
):
    """
    Обработка видео после генерации в основной рабочей генерации.
    Включает в себя работу с сообщениями, сохранением в стейт, генерацией и отправкой видео юзеру.

    Args:
        call: CallbackQuery - CallbackQuery с сообщением о генерации видео
        state: FSMContext - Контекст состояния
        model_name: str - Название модели для генерации видео
        prompt: str - Промпт для генерации видео
        type_for_video_generation: str - Тип генерации видео (Рабочий или Тестовый)
        image_url: str - Ссылка на изображение, из которого будет генерироваться видео
    """
    await state.update_data(prompt_for_video=prompt)

    redis_storage = get_redis_storage()
    task_dto = TaskProcessVideoDTO(
        user_id=call.from_user.id,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        callback_data=call.data,
        model_name=model_name,
        prompt=prompt,
        type_for_video_generation=type_for_video_generation,
        image_url=image_url,
    )
    await redis_storage.add_task(settings.PROCESS_VIDEO_TASK, task_dto)

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение про генерацию видео
    video_progress_message = await editMessageOrAnswer(
        call,
        text.GENERATE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index),
    )

    # Генерируем видео
    if settings.MOCK_MODE:
        video_path = "FocuuusBot/bot/assets/mocks/mock_video.mp4"
    else:
        try:
            video_path = await retryOperation(
                generate_video,
                10,
                1.5,
                prompt,
                image_url,
            )
        except Exception as e:
            # Отправляем сообщение об ошибке
            traceback.print_exc()
            logger.error(f"Произошла ошибка при генерации видео: {e}")
            await editMessageOrAnswer(
                call,
                text.GENERATE_VIDEO_ERROR_TEXT.format(
                    model_name,
                    model_name_index,
                    e,
                ),
                reply_markup=video_generation_keyboards.videoGenerationTypeKeyboard(
                    model_name,
                    False,
                    rewrite_prompt=True,
                ),
            )
            raise e

    if not video_path:
        await safe_send_message(
            text.GENERATE_VIDEO_ERROR_TEXT.format(
                model_name,
                model_name_index,
                "Не удалось сгенерировать видео",
            ),
            call,
            reply_markup=video_generation_keyboards.videoGenerationTypeKeyboard(
                model_name,
                False,
                rewrite_prompt=True,
            ),
        )
        return

    if isinstance(video_path, dict):
        if video_path.get("error"):
            await safe_send_message(
                text.GENERATE_VIDEO_ERROR_TEXT.format(
                    model_name,
                    model_name_index,
                    video_path.get("error"),
                ),
                call,
                reply_markup=video_generation_keyboards.videoGenerationTypeKeyboard(
                    model_name,
                    False,
                    rewrite_prompt=True,
                ),
            )
            return

    # Добавляем путь к видео в стейт
    data_for_update = {f"{model_name}": video_path}
    await appendDataToStateArray(state, "video_paths", data_for_update)

    # Отправляем видео юзеру
    video = types.FSInputFile(video_path)
    prefix = f"generate_video|{model_name}"

    if type_for_video_generation == "work":
        method = call.message.answer_video(
            video=video,
            caption=text.GENERATE_VIDEO_SUCCESS_TEXT.format(
                model_name,
                model_name_index,
            ),
            reply_markup=video_generation_keyboards.videoCorrectnessKeyboard(
                model_name,
            ),
        )
        video_message = await bot(method)
    else:  # При тестовой просто отправляем юзеру результат генерации
        method = call.message.answer_video(
            video=video,
            caption=text.GENERATE_TEST_VIDEO_SUCCESS_TEXT.format(
                model_name,
                model_name_index,
            ),
            reply_markup=video_generation_keyboards.generatedVideoKeyboard(
                prefix,
                False,
            ),
        )
        video_message = await bot(method)

    # Удаляем сообщение о генерации видео
    await video_progress_message.delete()

    # Сохраняем сообщение в стейт для последующего удаления
    data_for_update = {f"{model_name}": video_message.message_id}
    await appendDataToStateArray(
        state,
        "videoGeneration_messages_ids",
        data_for_update,
    )

    redis_storage = get_redis_storage()
    await redis_storage.delete_task(
        settings.PROCESS_VIDEO_TASK,
        key_for_video(
            type_for_video=type_for_video_generation,
            user_id=call.from_user.id,
            image_url=image_url,
            model_name=model_name,
        ),
    )
