from aiogram.fsm.context import FSMContext

from bot.logger import logger


async def deleteMessageFromState(
    state: FSMContext,
    key: str,
    model_name: str,
    chat_id: int,
    delete_keyboard_message: bool = False,
    image_index: int = None,
):
    """
    Удаляет все сообщения медиагруппы для model_name из state[key], поддерживает структуру с image_index.
    Если delete_keyboard_message=True, дополнительно удаляет сообщение с клавиатурой (например, для мультивыбора).
    """
    from bot.InstanceBot import (
        bot,  # импорт по месту, чтобы избежать циклов
    )

    state_data = await state.get_data()
    data_list = state_data.get(key, [])

    logger.info(f"[deleteMessageFromState] data_list: {data_list}, state_data: {state_data}")

    logger.info(f"[deleteMessageFromState] model_name: {model_name}, image_index: {image_index}")

    # Собираем только message_id медиагруппы (type == 'media' или без type)
    if image_index is None:
        messages_to_delete = [
            item["message_id"]
            for item in data_list
            if item.get("model_name") == model_name and (item.get("type") in (None, "media"))
        ]
    else:
        messages_to_delete = [
            item["message_id"]
            for item in data_list
            if item.get("model_name") == model_name and item.get("image_index") == image_index and (item.get("type") in (None, "media"))
        ]

    logger.info(
        f"[deleteMessageFromState] Найдено сообщений для удаления: {messages_to_delete}",
    )
    for msg_id in messages_to_delete:
        try:
            await bot.delete_message(chat_id, msg_id)
        except Exception as e:
            logger.warning(f"Не удалось удалить сообщение {msg_id}: {e}")

    # Очищаем их из стейта
    data_list = [
        item for item in data_list if not (
            item.get("model_name") == model_name and (item.get("type") in (None, "media"))
        )
    ]
    await state.update_data(**{key: data_list})
    logger.info(f"[deleteMessageFromState] После удаления: {data_list}")

    # Если явно нужно — удаляем сообщение с клавиатурой (например, для мультивыбора)
    if delete_keyboard_message:
        select_message_id = state_data.get("imageGeneration_select_message_id")
        if select_message_id:
            try:
                await bot.delete_message(chat_id, select_message_id)
                logger.info(f"[deleteMessageFromState] Удалено select_message_id: {select_message_id}")
            except Exception as e:
                logger.info(f"[deleteMessageFromState] Не удалось удалить select_message_id: {e}")
