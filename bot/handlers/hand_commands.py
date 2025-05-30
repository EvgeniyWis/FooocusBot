from aiogram import types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from config import ALLOWED_USERS
from InstanceBot import router
from keyboards import start_generation_keyboards
from utils import text


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    await state.set_state(None)

    if message.from_user.id not in ALLOWED_USERS:
        await message.answer(text.ACCESS_DENIED_TEXT)
        return
    
    # Очищаем стейт
    await state.update_data(stop_generation=False)
    await state.update_data(jobs={})
    await state.update_data(total_jobs_count=0)
    await state.update_data(model_name_for_generation=None)

    await message.answer(
        text.START_TEXT, reply_markup=start_generation_keyboards.generationsTypeKeyboard(),
    )


# Обработка команды /stop
async def stop_generation(message: types.Message, state: FSMContext):
    await state.update_data(stop_generation=True)
    await message.answer(text.STOP_GENERATION_TEXT, reply_markup=ReplyKeyboardRemove())


# DEV: получение file id видео
# async def get_file_id(message: types.Message):
#     if message.video:
#         await message.answer(message.video.file_id)


# Добавление обработчиков
def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart())

    router.message.register(stop_generation, Command("stop"))

    # DEV: получение file id видео
    # router.message.register(get_file_id)

