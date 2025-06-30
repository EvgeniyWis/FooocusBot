from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.helpers import text
from bot.helpers.generateImages.dataArray import getModelNameIndex
from bot.states import StartGenerationState
from bot.utils.handlers import appendDataToStateArray
from bot.utils.handlers.messages import editMessageOrAnswer


async def process_write_prompt(
    call: types.CallbackQuery,
    state: FSMContext,
    model_name: str,
    is_quick_generation: bool = False,
    is_nsfw_generation: bool = False,
):
    """
    Обработчик для записи промпта для видео генерации: установка стейта, отправка сообщения.

    Args:
        call: CallbackQuery - объект callback-запроса
        state: FSMContext - контекст состояния
        model_name: str - название модели
        is_quick_generation: bool - флаг быстрой генерации

    Returns:
        None
    """
    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    await state.update_data(model_name_for_video_generation=model_name)

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

    if call.message.content_type == types.ContentType.PHOTO:
        await call.message.edit_caption(
            caption=message_text,
        )
    else:
        await editMessageOrAnswer(
            call,
            message_text,
        )

    # Сохраняем в стейт сообщение о написании промпта для последующего удаления
    data_for_update = {f"{model_name}": call.message.message_id}
    await appendDataToStateArray(
        state,
        "write_prompt_messages_ids",
        data_for_update,
    )

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
