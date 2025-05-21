
from aiogram import types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.user import keyboards
from utils import text
from InstanceBot import router
from aiogram.filters import Command


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text.START_TEXT, reply_markup=keyboards.generationsTypeKeyboard()
    )


# Обработка команды /stop   
async def stop_generation(message: types.Message, state: FSMContext):
    await state.update_data(stop_generation=True)
    await message.answer(text.STOP_GENERATION_TEXT)


# Добавление обработчиков
def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart())

    router.message.register(stop_generation, Command("stop"))
