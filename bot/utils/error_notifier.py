import traceback
from datetime import datetime
from typing import Optional

from aiogram import types
from aiogram.types import TelegramObject
from zoneinfo import ZoneInfo

from bot.InstanceBot import bot
from bot.logger import logger
from bot.settings import settings


async def send_error_to_developers(
    error: Exception, 
    context: str, 
    event: TelegramObject,
    additional_info: Optional[str] = None
):
    """
    Отправляет ошибку разработчикам, но не прерывает выполнение для пользователя.
    
    Args:
        error: Exception - объект ошибки
        context: str - контекст, где произошла ошибка
        event: TelegramObject - объект события для получения информации о пользователе
        additional_info: Optional[str] - дополнительная информация об ошибке
    """
    try:
        # Формируем сообщение об ошибке
        error_message = "❌ Ошибка в процессе обработки:\n\n"
        error_message += f"🔴 Тип ошибки: {type(error).__name__}\n"
        error_message += f"📝 Описание: {str(error)}\n"
        error_message += f"📍 Контекст: {context}\n\n"
        
        if additional_info:
            error_message += f"ℹ️ Дополнительная информация: {additional_info}\n\n"
        
        moscow_time = datetime.now(ZoneInfo("Europe/Moscow")).strftime('%Y-%m-%d %H:%M:%S')
        error_message += f"🕒 Время ошибки: {moscow_time}\n\n"

        # Добавляем информацию о пользователе, если доступна
        if hasattr(event, "from_user"):
            user = event.from_user
            error_message += (
                f"👤 Пользователь: {user.full_name} (@{user.username})\n"
            )
            error_message += f"ID: {user.id}\n\n"
        elif hasattr(event, "message") and hasattr(event.message, "from_user"):
            user = event.message.from_user
            error_message += (
                f"👤 Пользователь: {user.full_name} (@{user.username})\n"
            )
            error_message += f"ID: {user.id}\n\n"

        # Добавляем traceback
        error_message += (
            f"📋 Traceback:\n<code>{traceback.format_exc()}</code>"
        )

        # Отправляем сообщение об ошибке разработчикам
        for DEV_CHAT_ID in settings.DEV_CHAT_IDS:
            await bot.send_message(DEV_CHAT_ID, error_message)
            
    except Exception as send_error:
        logger.error(
            f"Не удалось отправить сообщение об ошибке разработчикам: {send_error}",
        )


async def send_error_to_developers_with_callback(
    error: Exception, 
    context: str, 
    call: types.CallbackQuery,
    additional_info: Optional[str] = None
):
    """
    Отправляет ошибку разработчикам для callback query событий.
    
    Args:
        error: Exception - объект ошибки
        context: str - контекст, где произошла ошибка
        call: types.CallbackQuery - объект вызова для получения информации о пользователе
        additional_info: Optional[str] - дополнительная информация об ошибке
    """
    await send_error_to_developers(error, context, call, additional_info) 