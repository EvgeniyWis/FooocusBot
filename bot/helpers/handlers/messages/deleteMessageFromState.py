from aiogram.fsm.context import FSMContext

from bot.logger import logger


async def deleteMessageFromState(
    state: FSMContext,
    key: str,
    model_name: str,
    chat_id: int,
    delete_keyboard_message: bool = False,
    image_index: int = None,
    job_id: str = None,
):
    from bot.InstanceBot import bot

    state_data = await state.get_data()
    data_list = state_data.get(key, [])

    logger.info(
        f"[deleteMessageFromState] data_list: {data_list}, state_data: {state_data}",
    )
    logger.info(
        f"[deleteMessageFromState] model_name: {model_name}, image_index: {image_index}, job_id: {job_id}",
    )

    messages_to_delete = []
    for item in data_list:
        if item.get("model_name") != model_name:
            continue
        if item.get("type") not in (None, "media"):
            continue
        if job_id is not None and not item.get(
            "job_id",
            "",
        ).startswith(job_id):
            continue
        if image_index is not None and item.get("image_index") != image_index:
            continue
        messages_to_delete.append(item["message_id"])

    logger.info(
        f"[deleteMessageFromState] media для удаления: {messages_to_delete}",
    )
    for msg_id in messages_to_delete:
        try:
            await bot.delete_message(chat_id, msg_id)
        except Exception as e:
            logger.warning(
                f"[deleteMessageFromState] Не удалось удалить media {msg_id}: {e}",
            )

    if delete_keyboard_message:
        for item in data_list:
            if item.get("model_name") != model_name:
                continue
            if item.get("type") != "keyboard":
                continue
            if job_id is not None and not item.get(
                "job_id",
                "",
            ).startswith(job_id):
                continue
            select_message_id = item.get("message_id")
            try:
                await bot.delete_message(chat_id, select_message_id)
                logger.info(
                    f"[deleteMessageFromState] Удалено keyboard-сообщение {select_message_id}",
                )
            except Exception as e:
                logger.warning(
                    f"[deleteMessageFromState] Не удалось удалить keyboard {select_message_id}: {e}",
                )

    filtered_data_list = []
    for item in data_list:
        if item.get("model_name") != model_name:
            filtered_data_list.append(item)
            continue
        if item.get("type") not in (None, "media", "keyboard"):
            filtered_data_list.append(item)
            continue
        if job_id is not None and not item.get(
            "job_id",
            "",
        ).startswith(job_id):
            filtered_data_list.append(item)
            continue
        if image_index is not None and item.get("image_index") != image_index:
            filtered_data_list.append(item)
            continue

    await state.update_data(**{key: filtered_data_list})
    logger.info(
        f"[deleteMessageFromState] После удаления: {filtered_data_list}",
    )
