from aiogram import types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from utils.videoExamples.getVideoExampleDataByIndex import getVideoExampleDataByIndex
from utils.saveImages.getFolderDataByID import getFolderDataByID
from utils.generateImages.dataArray.getDataArrayWithRootPrompt import getDataArrayWithRootPrompt
from utils.saveImages.saveImage import saveImage
from utils.generateImages.generateImage import generateByData, generateTestImagesByAllSettings
from keyboards.user.keyboards import generationsAmountKeyboard, selectSettingKeyboard, generateVideoKeyboard, videoExampleKeyboard
from utils import text
from states import UserState
from utils.generateImages.generateImages import generateImages
from logger import logger
from InstanceBot import bot
import traceback
from utils.videoExamples.getVideoExamplesData import getVideoExamplesData

# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text.START_TEXT, reply_markup=generationsAmountKeyboard()
    )


# Обработка выбора количества генераций
async def choose_generations_amount(
    call: types.CallbackQuery, state: FSMContext
):
    generations_amount = call.data.split("|")[1]
    is_test_generation = generations_amount == "test"
    await state.update_data(generations_amount=generations_amount)

    await call.message.edit_text(
        text.GET_GENERATIONS_SUCCESS_TEXT,
        reply_markup=selectSettingKeyboard(is_test_generation),
    )


# Обработка выбора настройки
async def choose_setting(call: types.CallbackQuery, state: FSMContext):
    setting_number = call.data.split("|")[1]
    await state.update_data(setting_number=setting_number)
    await call.message.edit_text(
        text.GET_SETTINGS_WITH_TEST_GENERATIONS_SUCCESS_TEXT
    )
    await state.set_state(UserState.write_prompt)


# Обработка ввода промпта
async def write_prompt(message: types.Message, state: FSMContext):
    prompt = message.text
    user_id = message.from_user.id
    data = await state.get_data()
    is_test_generation = data["generations_amount"] == "test"
    setting_number = data["setting_number"]
    message_for_edit = await message.answer(
        text.TEST_GENERATION_GET_PROMPT_SUCCESS_TEXT
        if is_test_generation
        else text.GET_PROMPT_SUCCESS_TEXT
    )

    # Генерируем изображения
    try:
        if is_test_generation:
            if setting_number == "all":
                result = await generateTestImagesByAllSettings(message, state, user_id, is_test_generation, message_for_edit, False)
            else:
                # Прибавляем к каждому элементу массива корневой промпт
                dataArray = getDataArrayWithRootPrompt(int(setting_number), prompt)
                dataJSON = dataArray[0]["json"]
                model_name = dataArray[0]["model_name"]
                folder_id = dataArray[0]["folder_id"]
                result = [await generateByData(dataJSON, model_name, message, state, user_id, setting_number, folder_id, is_test_generation, False)]
        else:
            result = await generateImages(int(setting_number), prompt, message_for_edit, state, user_id, is_test_generation)

        if result:
            await message.answer(text.GENERATE_IMAGE_SUCCESS_TEXT)
        else:
            raise Exception("Произошла ошибка при генерации изображения")

    except Exception as e:
        traceback.print_exc()
        await message.answer(text.GENERATION_ERROR_TEXT)
        await state.clear()
        logger.error(f"Произошла ошибка при генерации изображения: {e}")
        return


# Обработка выбора изображения
async def select_image(call: types.CallbackQuery, state: FSMContext):
    # Получаем id пользователя
    user_id = call.from_user.id

    # Получаем индекс работы и индекс изображения
    model_name = call.data.split("|")[1]
    folder_id = call.data.split("|")[2]
    image_index = int(call.data.split("|")[3])

    # Получаем изображения из state
    data = await state.get_data()
    images = data[f"images_{model_name}"]

    # Получаем выбранное изображение
    chosen_image = images[int(image_index) - 1]

    # Сохраняем изображение
    image_index = int(image_index) - 1
    link = await saveImage(chosen_image, user_id, model_name, folder_id)

    # Получаем данные родительской папки
    folder = getFolderDataByID(folder_id)
    parent_folder_id = folder['parents'][0]
    parent_folder = getFolderDataByID(parent_folder_id)

    logger.info(f"Данные папки по id {folder_id}: {folder}")

    # Отправляем сообщение о сохранении изображения
    await call.message.edit_text(text.SAVE_IMAGES_SUCCESS_TEXT
    .format(link, model_name, parent_folder['webViewLink']), reply_markup=generateVideoKeyboard())

    # Удаляем отправленные изображения из чата
    try:    
        mediagroup_messages_ids = data[f"mediagroup_messages_ids_{model_name}"]
        chat_id = call.message.chat.id
        for message_id in mediagroup_messages_ids:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except:
        pass


# Обработка нажатия кнопки "📹 Сгенерировать видео"
async def start_generate_video(call: types.CallbackQuery):
    # Получаем id пользователя и удаляем сообщение
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(user_id, message_id)

    # Получаем все видео-шаблоны с их промптами
    templates_examples = await getVideoExamplesData()

    # Выгружаем видео-примеры вместе с их промптами
    for index, value in templates_examples.items():
        await bot.send_video(user_id, value["file"], caption=value["prompt"], reply_markup=videoExampleKeyboard(index))


# Обработка нажатия кнопок под видео-примером
async def handle_video_example_buttons(call: types.CallbackQuery):
    # Получаем индекс видео-примера и тип кнопки
    temp = call.data.split("|")
    index = temp[1]
    button_type = temp[2]

    # Получаем видео-пример по его индексу
    video_example_data = await getVideoExampleDataByIndex(index)

    if button_type == "test":
        pass



# Добавление обработчиков
def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart())

    router.callback_query.register(
        choose_generations_amount,
        lambda call: call.data.startswith("generations_amount"),
    )

    router.callback_query.register(
        choose_setting, lambda call: call.data.startswith("select_setting")
    )

    router.message.register(write_prompt, StateFilter(UserState.write_prompt))

    router.callback_query.register(select_image, lambda call: call.data.startswith("select_image"))

    router.callback_query.register(select_image, lambda call: call.data == "generate_video")

    router.callback_query.register(handle_video_example_buttons, lambda call: call.data.startswith("generate_video"))
