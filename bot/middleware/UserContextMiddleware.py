from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from bot.app.core.logging import current_user_id, current_username


class UserContextMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = None

        # Универсально пробуем вытащить пользователя из события
        if hasattr(event, "from_user") and getattr(event, "from_user") is not None:
            user = event.from_user
        elif hasattr(event, "message") and getattr(event.message, "from_user", None) is not None:
            user = event.message.from_user
        elif isinstance(event, CallbackQuery):
            user = event.from_user
        elif isinstance(event, Message):
            user = event.from_user

        if user is not None:
            token_id = current_user_id.set(str(user.id))
            token_username = current_username.set(user.username or "-")
            try:
                return await handler(event, data)
            finally:
                # Возвращаем контекст к предыдущему состоянию
                current_user_id.reset(token_id)
                current_username.reset(token_username)
        else:
            return await handler(event, data) 