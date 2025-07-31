import asyncio

from aiogram import types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.helpers import text
from bot.helpers.handlers.startGeneration.cancelImageGenerationJobs import (
    cancelImageGenerationJobs,
)
from bot.InstanceBot import commands_router
from bot.keyboards import start_generation_keyboards
from bot.settings import settings
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    await state.set_state(None)

    if message.from_user.id not in settings.ALLOWED_USERS:
        await safe_send_message(text.ACCESS_DENIED_TEXT, message)
        return

    # Получаем из стейта все ошибки, которые есть
    state_data = await state.get_data()

    # Получаем все данные с постфиксом _errors
    second_upscale_errors = state_data.get("second_upscale_errors", [])
    upscale_errors = state_data.get("upscale_errors", [])
    faceswap_errors = state_data.get("faceswap_errors", [])
    save_image_errors = state_data.get("save_image_errors", [])
    video_generation_errors = state_data.get("video_generation_errors", [])
    is_errors = any([upscale_errors, second_upscale_errors, faceswap_errors, save_image_errors, video_generation_errors])

    if is_errors:
        def format_errors(errors):
            return "\n".join([f"{error['model_name']} - {error['image_index']} изображение" for error in errors]) if errors else "Отсутствуют"

        errors_text = text.ERRORS_STATS_TEXT.format(
            format_errors(upscale_errors),
            format_errors(second_upscale_errors),
            format_errors(faceswap_errors),
            format_errors(save_image_errors),
            format_errors(video_generation_errors),
        )

        await safe_send_message(errors_text, message)


    # Отправляем сообщение с кнопками
    await safe_send_message(
        text.START_TEXT,
        message,
        reply_markup=start_generation_keyboards.generationsTypeKeyboard(),
    )


# Обработка команды /stop
async def stop_generation(message: types.Message, state: FSMContext):
    await safe_send_message(
        text.STOP_GENERATION_TEXT_WITH_WAITING,
        message,
        reply_markup=ReplyKeyboardRemove(),
    )

    # Начинаем отмену
    await state.update_data(stop_generation=True)
    await cancelImageGenerationJobs(state)

    # Завершаем отмену
    await asyncio.sleep(15)
    await safe_send_message(text.STOP_GENERATION_TEXT, message)
    await state.update_data(stop_generation=False)


# Добавление обработчиков
def hand_add():
    commands_router.message.register(start, StateFilter("*"), CommandStart())
    commands_router.message.register(stop_generation, Command("stop"))
