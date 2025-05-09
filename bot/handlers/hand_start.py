from aiogram import types
from InstanceBot import router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from utils.saveImages.saveImage import saveImage
from utils.saveImages.createFolder import createFolder
from utils.generateImages.generateImage import generateImage
from keyboards.userKeyboards import generationsAmountKeyboard
from utils import text
from states import UserState
from utils.generateImages.generateImages import generateImages
from logger import logger
from utils.generateImages.data_array.getDataArrayWithRootPrompt import dataArray
from InstanceBot import bot


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer(text.START_TEXT,  
    reply_markup=generationsAmountKeyboard(dataArrayLen=len(dataArray)))
    await state.set_state(UserState.write_folder_name)


# Обработка выбора количества генераций
async def choose_generations_amount(call: types.CallbackQuery, state: FSMContext):
    generations_amount = call.data.split("|")[1]
    await state.update_data(generations_amount=generations_amount)

    if generations_amount == "all":
        await call.message.edit_text(text.GET_GENERATIONS_SUCCESS_TEXT)
        await state.set_state(UserState.write_folder_name)
    else:
        await call.message.edit_text(text.GET_FOLDER_NAME_SUCCESS_TEXT)
        await state.set_state(UserState.write_prompt)


# Обработка ввода названия папки
async def write_folder_name(message: types.Message, state: FSMContext):
    folder_name = message.text
    await state.update_data(folder_name=folder_name)
    await message.answer(text.GET_FOLDER_NAME_SUCCESS_TEXT)
    await state.set_state(UserState.write_prompt)


# Обработка ввода промпта
async def write_prompt(message: types.Message, state: FSMContext):
    prompt = message.text
    user_id = message.from_user.id
    data = await state.get_data()
    is_test_generation = data["generations_amount"] == "test"
    message_for_edit = await message.answer(
    text.TEST_GENERATION_GET_PROMPT_SUCCESS_TEXT if is_test_generation else text.GET_PROMPT_SUCCESS_TEXT)
       
    if not is_test_generation:
        # Создаём папку для сохранения изображений
        folder = createFolder(data["folder_name"])
        await state.update_data(folder=folder)

    # Генерируем изображения
    try:
        if is_test_generation:
            result = [await generateImage(message, dataArray[0], state, None, 0, user_id, False)]
        else:
            result = await generateImages(prompt, message_for_edit, state, data["folder_name"], user_id)

        if result:
            await message_for_edit.edit_text(text.GENERATE_IMAGE_SUCCESS_TEXT)
        else:
            raise Exception("Произошла ошибка при генерации изображения")
        
    except Exception as e:
        await message.answer(text.GENERATION_ERROR_TEXT)
        await state.clear()
        logger.error(f"Произошла ошибка при генерации изображения: {e}")
        return


# Обработка выбора изображения
async def select_image(call: types.CallbackQuery, state: FSMContext):
    # Получаем id пользователя
    user_id = call.from_user.id

    # Получаем индекс работы и индекс изображения
    job_id = call.data.split("|")[1]
    image_index = call.data.split("|")[2]

    # Получаем изображения из state
    data = await state.get_data()
    images = data[f"images_{job_id}"]

    # Получаем выбранное изображение
    chosen_image = images[int(image_index) - 1]
        
    # Сохраняем изображение
    image_index = int(image_index) - 1
    folder = data["folder"]
    link = await saveImage(chosen_image, image_index, user_id, job_id, data["folder_name"], folder["id"])

    # Отправляем сообщение о сохранении изображения
    await call.message.edit_text(text.SAVE_IMAGES_SUCCESS_TEXT.format(data["folder_name"], link, folder['webViewLink']))

    # Удаляем отправленные изображения из чата
    mediagroup_messages_ids = data[f"mediagroup_messages_ids_{job_id}"]
    chat_id = call.message.chat.id
    for message_id in mediagroup_messages_ids:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)


# Добавление обработчиков
def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart())

    router.callback_query.register(choose_generations_amount, lambda call: call.data.startswith("generations_amount"))

    router.message.register(write_folder_name, StateFilter(UserState.write_folder_name))

    router.message.register(write_prompt, StateFilter(UserState.write_prompt))

    router.callback_query.register(select_image, lambda call: call.data.startswith("select_image"))
