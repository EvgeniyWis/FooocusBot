from aiogram.fsm.context import FSMContext

from bot.logger import logger


async def deleteMessageFromState(
    state: FSMContext,
    key: str,
    model_name: str,
    chat_id: int,
    delete_keyboard_message: bool = False,
    image_index: int = None,
    generation_id: str = None,
):
    from bot.InstanceBot import bot

    state_data = await state.get_data()
    data_list = state_data.get(key, [])

    logger.info(
        f"[deleteMessageFromState] data_list: {data_list}, state_data: {state_data}",
    )
    logger.info(
        f"[deleteMessageFromState] model_name: {model_name}, image_index: {image_index}, generation_id: {generation_id}",
    )

    # Фильтрация сообщений по model_name, image_index и generation_id (если есть)
    if image_index is None:
        messages_to_delete = [
            item["message_id"]
            for item in data_list
            if item.get("model_name") == model_name
            and (item.get("type") in (None, "media"))
            and (
                generation_id is None
                or item.get("generation_id") == generation_id
            )
        ]
    else:
        messages_to_delete = [
            item["message_id"]
            for item in data_list
            if item.get("model_name") == model_name
            and item.get("image_index") == image_index
            and (item.get("type") in (None, "media"))
            and (
                generation_id is None
                or item.get("generation_id") == generation_id
            )
        ]

    logger.info(
        f"[deleteMessageFromState] Найдено сообщений для удаления: {messages_to_delete}",
    )
    for msg_id in messages_to_delete:
        try:
            await bot.delete_message(chat_id, msg_id)
        except Exception as e:
            logger.warning(f"Не удалось удалить сообщение {msg_id}: {e}")

    # Удаляем сообщение с клавиатурой, если нужно
    if delete_keyboard_message:
        select_message_id = None
        select_messages = [
            item
            for item in data_list
            if item.get("model_name") == model_name
            and item.get("type") == "keyboard"
            and (
                generation_id is None
                or item.get("generation_id") == generation_id
            )
        ]
        if select_messages:
            select_message_id = select_messages[-1]["message_id"]
        else:
            # fallback если нет generation_id
            select_message_id = state_data.get(
                "imageGeneration_select_message_id"
            )

        if select_message_id:
            try:
                await bot.delete_message(chat_id, select_message_id)
                logger.info(
                    f"[deleteMessageFromState] Удалено select_message_id: {select_message_id}"
                )
            except Exception as e:
                logger.info(
                    f"[deleteMessageFromState] Не удалось удалить select_message_id: {e}"
                )

    # Фильтруем data_list от media и keyboard за один проход
    filtered_data_list = [
        item
        for item in data_list
        if not (
            item.get("model_name") == model_name
            and item.get("type") in (None, "media", "keyboard")
            and (
                generation_id is None
                or item.get("generation_id") == generation_id
            )
        )
    ]

    await state.update_data(**{key: filtered_data_list})
    logger.info(
        f"[deleteMessageFromState] После удаления: {filtered_data_list}"
    )
