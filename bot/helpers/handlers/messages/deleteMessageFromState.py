from aiogram.fsm.context import FSMContext

from bot.InstanceBot import bot
from bot.logger import logger
from bot.utils.handlers.getDataInDictsArray import getDataInDictsArray


# Функция для удаления сообщения, полученного из стейта
async def deleteMessageFromState(
    state: FSMContext, key: str, model_name: str, chat_id: int,
):
    # Получаем сообщение из стейта
    state_data = await state.get_data()
    messages_ids = state_data.get(key, [])
    logger.info(
        f"Стейт сообщений для модели {model_name} по ключу {key}: {messages_ids}",
    )

    data = await getDataInDictsArray(messages_ids, model_name)

    if data is None:
        logger.warning(
            f"Не найдены сообщения для модели {model_name} по ключу {key} в стейте {state_data}",
        )
        return

    # Проверяем, data это массив или id один, и в зависимости от этого удаляем сообщение или сообщения
    try:
        if isinstance(data, list):
            for message_id in data:
                if isinstance(message_id, int):
                    try:
                        await bot.delete_message(chat_id, message_id)
                    except Exception as e:
                        logger.error(
                            f"Ошибка при удалении сообщения {message_id}: {e}",
                        )
        else:
            if isinstance(data, int):
                try:
                    await bot.delete_message(chat_id, data)
                except Exception as e:
                    logger.error(f"Ошибка при удалении сообщения {data}: {e}")
    except Exception as e:
        logger.error(f"Ошибка при удалении сообщения из стейта: {e}")

    # Удаляем сообщение из стейта
    messages_ids = [
        ids_dict
        for ids_dict in messages_ids
        if model_name not in ids_dict.keys()
    ]
    logger.info(
        f"Стейт сообщений по ключу {key} для модели {model_name} после удаления: {messages_ids}",
    )
    await state.update_data(**{key: messages_ids})
