from aiogram import types
from InstanceBot import router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from utils.saveImages import save_images
from utils import text
from states import UserState
from utils.generateImages.generateImages import generateImages
from logger import logger


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    await message.answer(text.START_TEXT)
    await state.set_state(UserState.write_folder_name)


# Обработка ввода названия папки
async def write_folder_name(message: types.Message, state: FSMContext):
    folder_name = message.text
    await state.update_data(folder_name=folder_name)
    await message.answer(text.GET_FOLDER_NAME_SUCCESS_TEXT)
    await state.set_state(UserState.write_prompt)


# Обработка ввода промпта
async def write_prompt(message: types.Message, state: FSMContext):
    prompt = message.text
    message_for_edit = await message.answer(text.GET_PROMPT_SUCCESS_TEXT)
    data = await state.get_data()

    try:
        images = await generateImages(prompt, message_for_edit, state, data["folder_name"])

        if images:
            await message_for_edit.edit_text(text.GENERATE_IMAGE_SUCCESS_TEXT.format(data["folder_name"]))
            await state.set_state(UserState.write_folder_name)
            await state.update_data(images=images)

    except Exception as e:
        await message.answer("Произошла ошибка при генерации изображения")
        await state.clear()
        logger.error(f"Произошла ошибка при генерации изображения: {e}")
    
    folder_link = await save_images(images, data["folder_name"])

    if folder_link:
        await message.answer(text.SAVE_IMAGES_SUCCESS_TEXT.format(data["folder_name"], folder_link))
        
    await state.clear()


# Добавление обработчиков
def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart())

    router.message.register(write_folder_name, StateFilter(UserState.write_folder_name))

    router.message.register(write_prompt, StateFilter(UserState.write_prompt))
