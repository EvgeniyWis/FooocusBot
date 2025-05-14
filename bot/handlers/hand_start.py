from utils.generateImages.dataArray.getDataArrayBySettingNumber import getDataArrayBySettingNumber
from utils.videos.generateVideo import generateVideo
from utils.facefusion.facefusion_swap import facefusion_swap
from aiogram import types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from utils.videoExamples.getVideoExampleDataByIndex import getVideoExampleDataByIndex
from utils.saveImages.getFolderDataByID import getFolderDataByID
from utils.generateImages.dataArray.getDataArrayWithRootPrompt import getDataArrayWithRootPrompt
from utils.saveFile import saveFile
from utils.generateImages.generateImage import generateByData, generateTestImagesByAllSettings
from keyboards.user.keyboards import generationsTypeKeyboard, selectSettingKeyboard, generateVideoKeyboard, videoCorrectnessKeyboard, videoExampleKeyboard
from utils import text
from states import UserState
from utils.generateImages.generateImages import generateImages
from logger import logger
from InstanceBot import bot
import traceback
from utils.videoExamples.getVideoExamplesData import getVideoExamplesData
from InstanceBot import router
import os
import asyncio


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text.START_TEXT, reply_markup=generationsTypeKeyboard()
    )


# Обработка выбора количества генераций
async def choose_generations_type(
    call: types.CallbackQuery, state: FSMContext
):
    generations_type = call.data.split("|")[1]
    is_test_generation = generations_type == "test"
    await state.update_data(generations_type=generations_type)

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
    await state.set_state(UserState.write_prompt_for_image)


# Обработка ввода промпта
async def write_prompt(message: types.Message, state: FSMContext):
    prompt = message.text
    user_id = message.from_user.id
    data = await state.get_data()
    is_test_generation = data["generations_type"] == "test"
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
                picture_folder_id = dataArray[0]["picture_folder_id"]
                video_folder_id = dataArray[0]["video_folder_id"]
                result = [await generateByData(dataJSON, model_name, message, state, user_id, setting_number, picture_folder_id, video_folder_id, is_test_generation, False)]
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
    image_index = int(call.data.split("|")[2])

    # Получаем данные из стейта
    data = await state.get_data()
    setting_number = int(data["setting_number"])

    # Получаем данные генерации по названию модели
    dataArray = getDataArrayBySettingNumber(setting_number)
    data = next((data for data in dataArray if data["model_name"] == model_name), None)
    picture_folder_id = data["picture_folder_id"]
    video_folder_id = data["video_folder_id"]

    # Сохраняем название модели и id папки для видео
    await state.update_data(model_name=model_name)
    await state.update_data(video_folder_id=video_folder_id)

    # Меняем текст на сообщении
    await call.message.edit_text(text.FACE_SWAP_PROGRESS_TEXT.format(image_index))

    # Заменяем лицо на исходном изображении, которое сгенерировалось, на лицо с изображения модели
    faceswap_target_path = f"images/temp/{model_name}_{user_id}/{image_index}.jpg"
    faceswap_source_path = f"images/faceswap/{model_name}.jpg"
    logger.info(f"Путь к исходному изображению для замены лица: {faceswap_target_path}")
    logger.info(f"Путь к целевому изображению для замены лица: {faceswap_source_path}")

    max_attempts = 5
    attempt = 0
    while True:
        attempt += 1
        try:
            result_path = await facefusion_swap(faceswap_source_path, faceswap_target_path)
            break
        except Exception as e:
            traceback.print_exc()
            logger.error(f"Произошла ошибка при замене лица: {e}")
            if attempt >= max_attempts:
                await call.message.answer(text.FACE_SWAP_ERROR_TEXT)
                raise Exception(f"Не удалось сделать генерацию лица после {max_attempts} попыток")
            await asyncio.sleep(20)

    logger.info(f"Результат замены лица: {result_path}")

    # Меняем текст на сообщении
    await call.message.edit_text(text.SAVE_IMAGE_PROGRESS_TEXT.format(image_index))

    # Сохраняем изображение
    image_index = int(image_index) - 1
    link = await saveFile(result_path, user_id, model_name, picture_folder_id)

    # Получаем данные родительской папки
    folder = getFolderDataByID(picture_folder_id)
    parent_folder_id = folder['parents'][0]
    parent_folder = getFolderDataByID(parent_folder_id)

    logger.info(f"Данные папки по id {picture_folder_id}: {folder}")

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

    # Удаляем изображение с заменённым лицом
    os.remove(result_path)


# Обработка нажатия кнопки "📹 Сгенерировать видео"
async def start_generate_video(call: types.CallbackQuery):
    # Получаем id пользователя и удаляем сообщение
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(user_id, message_id)

    # Отправляем сообщение для выбора видео-примеров
    await call.message.answer(text.SELECT_VIDEO_EXAMPLE_TEXT)

    # Получаем все видео-шаблоны с их промптами
    templates_examples = await getVideoExamplesData()

    # Выгружаем видео-примеры вместе с их промптами
    for index, value in templates_examples.items():
        video = types.FSInputFile(value["file_path"])
        await call.message.answer_video(
            video=video,
            caption=value["prompt"],
            reply_markup=videoExampleKeyboard(index)
        )


# Обработка нажатия кнопок под видео-примером
async def handle_video_example_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем индекс видео-примера и тип кнопки
    temp = call.data.split("|")
    index = int(temp[1])
    button_type = temp[2]

    # Получаем название модели
    data = await state.get_data()
    model_name = data["model_name"]

    # Получаем данные видео-примера по его индексу
    video_example_data = await getVideoExampleDataByIndex(index)

    # Получаем кастомный промпт, если он есть, а если нет, то берем промпт из видео-примера 
    if "prompt_for_video" in data:
        custom_prompt = data["prompt_for_video"]
    else:
        custom_prompt = None
    video_example_prompt = custom_prompt if custom_prompt else video_example_data["prompt"]

    # Получаем путь к видео-примеру
    video_example_file_path = video_example_data["file_path"]

    # Генерируем видео
    video_url = await generateVideo(video_example_prompt, video_example_file_path)
    
    # Сохраняем видео в стейт
    await state.update_data(video_url=video_url)

    # Отправляем видео
    if button_type == "test":
        video = types.FSInputFile(video_url)
        await call.message.answer_video(video=video, caption=text.GENERATE_TEST_VIDEO_SUCCESS_TEXT, 
        reply_markup=videoExampleKeyboard(index, False))

    elif button_type == "work":
        video = types.FSInputFile(video_url)
        await call.message.answer_video(video=video, caption=text.GENERATE_VIDEO_SUCCESS_TEXT.format(model_name), 
        reply_markup=videoCorrectnessKeyboard())

    elif button_type == "write_prompt":
        await state.update_data(video_example_file_path=video_example_file_path)
        await state.update_data(video_example_index=index)
        await call.message.answer(text.WRITE_PROMPT_FOR_VIDEO_TEXT)
        await state.set_state(UserState.write_prompt_for_video)


# Хедлер для обработки ввода кастомного промпта для видео
async def write_prompt_for_video(message: types.Message, state: FSMContext):
    # Получаем данные
    prompt = message.text
    await state.update_data(prompt_for_video=prompt)
    data = await state.get_data()
    video_example_file = data["video_example_file"]
    index = data["video_example_index"]

    await message.answer_video(video_example_file, 
    caption=text.WRITE_PROMPT_FOR_VIDEO_SUCCESS_TEXT.format(prompt),
    reply_markup=videoExampleKeyboard(index, with_write_prompt=False))


# Обработка нажатия на кнопки корректности видео
async def handle_video_correctness_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем тип кнопки
    temp = call.data.split("|")
    button_type = temp[1]

    # Получаем данные
    data = await state.get_data()
    video_url = data["video_url"]
    user_id = call.from_user.id
    model_name = data["model_name"]
    video_folder_id = data["video_folder_id"]

    if button_type == "correct":
        link = await saveFile(video_url, user_id, model_name, video_folder_id, False)

    elif button_type == "incorrect":
        pass


# Добавление обработчиков
def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart())

    router.callback_query.register(
        choose_generations_type,
        lambda call: call.data.startswith("generations_type"),
    )

    router.callback_query.register(
        choose_setting, lambda call: call.data.startswith("select_setting")
    )

    router.message.register(write_prompt, StateFilter(UserState.write_prompt_for_image))

    router.callback_query.register(select_image, lambda call: call.data.startswith("select_image"))

    router.callback_query.register(start_generate_video, lambda call: call.data == "generate_video")

    router.callback_query.register(handle_video_example_buttons, lambda call: call.data.startswith("generate_video"))

    router.message.register(write_prompt_for_video, StateFilter(UserState.write_prompt_for_video))

    router.callback_query.register(handle_video_correctness_buttons, 
    lambda call: call.data.startswith("video_correctness"))