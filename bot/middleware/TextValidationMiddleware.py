from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from bot.helpers.handlers.messages.send_progress_message import (
    safe_send_message,
)
from bot.logger import logger


class TextValidationMiddleware(BaseMiddleware):
    """
    Middleware для проверки наличия текста в сообщениях.
    Работает только для хендлеров, которые ожидают текстовые сообщения.
    """
    
    def __init__(self, error_message: str = "❗️ Пожалуйста, отправьте текстовое сообщение."):
        self.error_message = error_message
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Проверяем, что это сообщение
        if not isinstance(event, Message):
            return await handler(event, data)
        
        # Получаем текущее состояние из данных
        state = data.get("state")
        if not state:
            return await handler(event, data)
        
        # Получаем текущее состояние
        current_state = await state.get_state()
        if not current_state:
            return await handler(event, data)
        
        # Список состояний, которые ожидают только текстовые сообщения
        text_only_states = [
            # Состояния для генерации изображений
            "StartGenerationState:write_prompt_for_images",
            "StartGenerationState:write_new_prompt_for_regenerate_image",
            "StartGenerationState:write_models_for_specific_generation",
            "StartGenerationState:write_multi_prompts_for_models",
            
            # Состояния для img2video
            "StartGenerationState:write_single_prompt_for_img2video",
            "StartGenerationState:ask_for_model_index_for_img2video",
            "StartGenerationState:collecting_prompt_parts_for_img2video",
            
            # Состояния для видео
            "StartGenerationState:write_prompt_for_video",
            "StartGenerationState:write_prompt_for_quick_video_generation",
            "StartGenerationState:write_prompt_for_video_generation_by_one_prompt",
            
            # Состояния для NSFW видео
            "StartGenerationState:write_prompt_for_nsfw_generation",
            "StartGenerationState:ask_video_length_input",
            
            # Состояния для рандомайзера
            "RandomizerState:write_variable_for_randomizer",
            "RandomizerState:write_value_for_variable_for_randomizer",
            "RandomizerState:write_one_message_for_randomizer",
            "RandomizerState:write_multi_messages_for_prompt_for_randomizer",
            
            # Состояния для многострочного ввода
            "MultiPromptInputState:collecting_model_prompts_for_groups",
            "MultiPromptInputState:collecting_prompt_parts",
        ]
        
        # Проверяем, является ли текущее состояние одним из тех, что ожидают только текст
        if current_state in text_only_states and event.text is None:
            logger.info(f"TextValidationMiddleware: Блокируем сообщение без текста в состоянии {current_state}")
            await safe_send_message(
                self.error_message,
                event,
            )
            return

        return await handler(event, data)
