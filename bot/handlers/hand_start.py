from aiogram import types
from InstanceBot import router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from utils import text
from states import UserState
from utils.generateImages import generateImages


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    await message.answer(text.START_TEXT)
    await state.set_state(UserState.write_prompt)


# Обработка ввода промпта
async def write_prompt(message: types.Message, state: FSMContext):
    prompt = message.text
    message_for_edit = await message.answer(text.GET_PROMPT_SUCCESS_TEXT)

    try:
        image = await generateImages(prompt, message_for_edit)

        if image:
            await message_for_edit.delete()
            await message.answer(text.GENERATE_IMAGE_SUCCESS_TEXT)

    except Exception as e:
        await message.answer("Произошла ошибка при генерации изображения")
        print(f"Ошибка: {e}")

    await state.clear()


def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart())

    router.message.register(write_prompt, StateFilter(UserState.write_prompt))

