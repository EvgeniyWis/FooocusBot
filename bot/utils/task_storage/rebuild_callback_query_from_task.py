from datetime import datetime

from aiogram.types import CallbackQuery, Chat, Message, User

from bot.domain.entities.task import TaskProcessImageDTO


def rebuild_callback_query_from_task(
    task: TaskProcessImageDTO,
) -> CallbackQuery:
    user = User(id=task.user_id, is_bot=False, first_name="User")
    chat = Chat(
        id=task.chat_id,
        type="private",
    )
    message = Message(
        message_id=task.message_id,
        date=datetime.now(),
        chat=chat,
    )
    return CallbackQuery(
        id="dummy",
        from_user=user,
        chat_instance="dummy",
        message=message,
        data=task.callback_data,
    )
