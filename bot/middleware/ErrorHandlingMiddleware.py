import traceback
from collections.abc import Awaitable
from typing import Any, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.InstanceBot import bot
from bot.logger import logger
from bot.utils.error_notifier import send_error_to_developers
from bot.utils.httpx.error_texts import PAYMENT_RUNPOD_ERROR_TEXT
from bot.utils.videos.errors_texts import (
    PROMPT_NOT_PASSED_MODERATION_ERROR_TEXT,
)


class ErrorHandlingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            if str(e) in [PAYMENT_RUNPOD_ERROR_TEXT]:
                return

            # Логируем ошибку
            logger.error(
                f"Ошибка: {str(e)}\nTraceback: {traceback.format_exc()}",
            )

            try:
                # Отправляем ошибку разработчикам используя новую утилиту
                await send_error_to_developers(
                    e, 
                    "ErrorHandlingMiddleware", 
                    event,
                    f"Handler: {handler.__name__ if hasattr(handler, '__name__') else 'Unknown'}"
                )

                # Если ошибка произошла в чате с пользователем, отправляем ему сообщение
                if hasattr(event, "chat") and str(e) not in [PROMPT_NOT_PASSED_MODERATION_ERROR_TEXT]:
                    await bot.send_message(
                        event.chat.id,
                        "😔 Произошла ошибка при обработке вашего запроса. "
                        "Администратор уже уведомлен о проблеме.",
                    )
            except Exception as send_error:
                logger.error(
                    f"Не удалось отправить сообщение об ошибке: {send_error}",
                )

            # Пробрасываем исходную ошибку дальше
            raise
