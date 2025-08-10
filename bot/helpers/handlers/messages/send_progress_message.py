from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.app.core.logging import logger
from bot.utils.handlers import appendDataToStateArray, getDataInDictsArray
from bot.utils.handlers.messages import safe_edit_message, safe_send_message


async def send_progress_message(state: FSMContext, array_key: str, model_name: str,
    message: types.Message, message_text: str, image_index: int, message_id_for_edit: int = None):
    """
    Отправляет сообщение о прогрессе генерации видео (если ещё не отправлено)

    Attributes:
        state (FSMContext): контекст состояния
        array_key (str): ключ массива в стейте
        model_name (str): имя модели
        message (types.Message): сообщение
        message_text (str): текст сообщения
        image_index (int): индекс изображения
        message_id_for_edit (int): id сообщения для редактирования (при необходимости)

    Returns:
        message_id (int): id сообщения о прогрессе
    """

    # Отправляем сообщение про генерацию видео (если ещё не отправлено)
    state_data = await state.get_data()
    messages = state_data.get(array_key, [])
    message_is_exist = any(item.get("model_name") == model_name and item.get("image_index") == image_index for item in messages)

    if not message_is_exist:
        if message_id_for_edit:
            try:
                message = await safe_edit_message(
                        message,
                        message_text,
                    )
            except Exception as e:
                logger.error(f"Ошибка при редактировании сообщения: {e}")
                message = await safe_send_message(
                    message_text,
                    message,
                )
        else:
            message = await safe_send_message(
                message_text,
                message,
            )

        # Проверяем, что message существует и имеет message_id
        if message and hasattr(message, 'message_id'):
            message_id = message.message_id
        else:
            logger.warning('message не существует или не содержит message_id, пробую отправить заново')
            message = await safe_send_message(
                message_text,
                message,
            )
            if message and hasattr(message, 'message_id'):
                message_id = message.message_id
            else:
                logger.error('Не удалось отправить сообщение повторно')
                message_id = None

        # Добавляем в массив с тем, для каких моделей отправлены сообщения о прогрессе
        data_for_update = {
            "model_name": model_name,
            "image_index": image_index,
            "message_id": message_id,
        }
        await appendDataToStateArray(state, array_key, data_for_update)

    else: # Если сообщение о начале upscale уже отправлено, то получаем его id
        message_id = await getDataInDictsArray(messages, model_name, image_index)

    return message_id







