from aiogram import types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from config import ALLOWED_USERS
from InstanceBot import router
from keyboards import start_generation_keyboards
from utils import text
from utils.handlers.startGeneration.cancelImageGenerationJobs import cancelImageGenerationJobs
import asyncio


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    await state.set_state(None)

    if message.from_user.id not in ALLOWED_USERS:
        await message.answer(text.ACCESS_DENIED_TEXT)
        return

    # Отправляем сообщение с кнопками
    await message.answer(
        text.START_TEXT, reply_markup=start_generation_keyboards.generationsTypeKeyboard(),
    )


# Обработка команды /stop
async def stop_generation(message: types.Message, state: FSMContext):
    await message.answer(text.STOP_GENERATION_TEXT_WITH_WAITING, reply_markup=ReplyKeyboardRemove())
    
    # Начинаем отмену
    await state.update_data(stop_generation=True)
    await cancelImageGenerationJobs(state)

    # Завершаем отмену
    await message.answer(text.STOP_GENERATION_TEXT, reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(5)
    await state.update_data(stop_generation=False)


# Обработка команды /clear
async def clear_state(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text.STATE_CLEARED_TEXT)


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


