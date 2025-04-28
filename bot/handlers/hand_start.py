from aiogram import types
from InstanceBot import router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from utils import text
from states import UserState

# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    await message.answer(text.START_TEXT)
    await state.set_state(UserState.write_prompt)

    await state.clear()


# Обработка ввода промпта
async def write_prompt(message: types.Message, state: FSMContext):
    await message.answer(text.GET_PROMPT_SUCCESS_TEXT)
    await state.set_state(UserState.write_prompt)


def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart())
