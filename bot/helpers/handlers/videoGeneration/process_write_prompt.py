from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.helpers import text
from bot.helpers.generateImages.dataArray import getModelNameIndex
from bot.logger import logger
from bot.states import StartGenerationState
from bot.utils.handlers import appendDataToStateArray
from bot.utils.handlers.messages import editMessageOrAnswer


async def process_write_prompt(
    call: types.CallbackQuery,
    state: FSMContext,
    model_name: str,
    image_index: int | None = None,
    is_quick_generation: bool = False,
    is_nsfw_generation: bool = False,
):
    """
    Обработчик для записи промпта для видео генерации: установка стейта, отправка сообщения.

    Args:
        call: CallbackQuery - объект callback-запроса
        state: FSMContext - контекст состояния
        model_name: str - название модели
        image_index: int | None - индекс изображения
        is_quick_generation: bool - флаг быстрой генерации
        is_nsfw_generation: bool - флаг генерации NSFW

    Returns:
        None
    """
    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    await state.update_data(model_name_for_video_generation=model_name)
    await state.update_data(image_index_for_video_generation=image_index)

    message_text = (
        text.WRITE_PROMPT_FOR_VIDEO_TEXT.format(
            model_name,
            model_name_index,
        )
        if not is_nsfw_generation
        else text.WRITE_PROMPT_FOR_NSFW_VIDEO_TEXT.format(
            model_name,
            model_name_index,
        )
    )

    write_prompt_message = None
    if call.message.content_type in [
        types.ContentType.PHOTO,
        types.ContentType.VIDEO,
    ]:
        try:
            write_prompt_message = await call.message.edit_caption(
                    caption=message_text,
                )
        except Exception as e:
            logger.error(f"Ошибка при редактировании сообщения: {e}")
    else:
        write_prompt_message = await editMessageOrAnswer(
            call,
            message_text,
        )

    # Сохраняем в стейт сообщение о написании промпта для последующего удаления
    if write_prompt_message:
        if image_index is not None:
            data_for_update = {
                "model_name": model_name,
                "image_index": image_index,
                "message_id": write_prompt_message.message_id,
            }
            await appendDataToStateArray(
                state,
                "write_prompt_messages_ids",
                data_for_update,
                unique_keys=("model_name", "image_index"),
            )
        else:
            data_for_update = {
                "model_name": model_name,
                "message_id": write_prompt_message.message_id,
            }
            await appendDataToStateArray(
                state,
                "write_prompt_messages_ids",
                data_for_update,
                unique_keys=("model_name"),
            )

    # Проверяем, добавилось ли имя модели в стейт
    state_data = await state.get_data()
    model_name_for_video_generation = state_data.get("model_name_for_video_generation", "")
    if model_name_for_video_generation != model_name:
        await state.update_data(model_name_for_video_generation=model_name)

    # Переключаем стейт
    if is_quick_generation:
        await state.set_state(
            StartGenerationState.write_prompt_for_quick_video_generation,
        )
    elif is_nsfw_generation:
        await state.set_state(
            StartGenerationState.write_prompt_for_nsfw_generation,
        )
    else:
        await state.set_state(StartGenerationState.write_prompt_for_video)
