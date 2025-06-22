from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.utils.handlers import appendDataToStateArray, getDataInDictsArray
from bot.utils.handlers.messages import safe_edit_message, safe_send_message


async def send_progress_message(state: FSMContext, array_key: str, model_name: str,
    message: types.Message, message_text: str, message_id_for_edit: int = None):
    """
    Отправляет сообщение о прогрессе генерации видео (если ещё не отправлено)

    Attributes:
        state (FSMContext): контекст состояния
        array_key (str): ключ массива в стейте
        model_name (str): имя модели
        message (types.Message): сообщение
        message_text (str): текст сообщения
        message_id_for_edit (int): id сообщения для редактирования (при необходимости)

    Returns:
        message_id (int): id сообщения о прогрессе
    """

    # Отправляем сообщение про генерацию видео (если ещё не отправлено)
    state_data = await state.get_data()
    messages = state_data.get(array_key, [])
    model_names = [item["model_name"] for item in messages]

    if model_name not in model_names:
        if message_id_for_edit:
            message = await safe_edit_message(
                message,
                message_text,
            )
        else:
            message = await safe_send_message(
                message_text,
                message,
            )

        message_id = message.message_id

        # Добавляем в массив с тем, для каких моделей отправлены сообщения о прогрессе
        data_for_update = {
            "model_name": model_name,
            "message_id": message_id,
        }
        await appendDataToStateArray(state, array_key, data_for_update)

    else: # Если сообщение о начале upscale уже отправлено, то получаем его id
        message_id = await getDataInDictsArray(messages, model_name)

    return message_id







