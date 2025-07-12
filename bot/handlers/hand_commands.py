import asyncio

from aiogram import types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.helpers import text
from bot.helpers.handlers.startGeneration.cancelImageGenerationJobs import (
    cancelImageGenerationJobs,
)
from bot.InstanceBot import router
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


# Обработка команды /clear
async def clear_state(message: types.Message, state: FSMContext):
    await state.clear()
    await safe_send_message(text.STATE_CLEARED_TEXT, message)


# DEV: получение file id видео
# async def get_file_id(message: types.Message):
#     if message.video:
#         await message.answer(message.video.file_id)


# Добавление обработчиков
def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart())

    router.message.register(stop_generation, Command("stop"))

    router.message.register(clear_state, Command("clear"))

    # DEV: получение file id видео
    # router.message.register(get_file_id)
