import traceback
from collections.abc import Awaitable
from datetime import datetime
from typing import Any, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from zoneinfo import ZoneInfo

from bot.InstanceBot import bot
from bot.logger import logger
from bot.settings import settings


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
            # Формируем сообщение об ошибке
            error_message = "❌ Произошла ошибка:\n\n"
            error_message += f"🔴 Тип ошибки: {type(e).__name__}\n"
            error_message += f"📝 Описание: {str(e)}\n\n"
            moscow_time = datetime.now(ZoneInfo("Europe/Moscow")).strftime('%Y-%m-%d %H:%M:%S')
            error_message += f"🕒 Время ошибки: {moscow_time}\n\n"

            # Добавляем информацию о пользователе, если доступна
            if hasattr(event, "from_user"):
                user = event.from_user
                error_message += (
                    f"👤 Пользователь: {user.full_name} (@{user.username})\n"
                )
                error_message += f"ID: {user.id}\n\n"

            # Добавляем traceback
            error_message += (
                f"📋 Traceback:\n<code>{traceback.format_exc()}</code>"
            )

            # Логируем ошибку
            logger.error(
                f"Ошибка: {str(e)}\nTraceback: {traceback.format_exc()}",
            )

            try:
                # Отправляем сообщение об ошибке разработчикам
                for DEV_CHAT_ID in settings.DEV_CHAT_IDS:
                    await bot.send_message(DEV_CHAT_ID, error_message)

                # Если ошибка произошла в чате с пользователем, отправляем ему сообщение
                if hasattr(event, "chat"):
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
