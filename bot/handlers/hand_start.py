from utils import retryOperation
from utils.generateImages.dataArray.getDataArrayBySettingNumber import getDataArrayBySettingNumber
from utils.videos.generateVideo import generateVideo
from utils.facefusion.facefusion_swap import facefusion_swap
from aiogram import types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from utils.videoExamples.getVideoExampleDataByIndex import getVideoExampleDataByIndex
from utils.saveImages.getFolderDataByID import getFolderDataByID
from utils.generateImages.dataArray.getDataArrayWithRootPrompt import getDataArrayWithRootPrompt
from utils.files.saveFile import saveFile
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
from datetime import datetime


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
                result = [await generateByData(dataJSON, model_name, message, state, user_id, setting_number, is_test_generation, False)]
        else:
            result = await generateImages(int(setting_number), prompt, message_for_edit, state, user_id, is_test_generation)

        if result:
            await message.answer(text.GENERATE_IMAGE_SUCCESS_TEXT)
        else:
            raise Exception("Произошла ошибка при генерации изображения")

    except Exception as e:
        traceback.print_exc()
        await message.answer(text.GENERATION_IMAGE_ERROR_TEXT)
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
    stateData = await state.get_data()
    setting_number = int(stateData["setting_number"])

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

    result_path = await retryOperation(facefusion_swap, 5, 2, faceswap_source_path, faceswap_target_path)

    logger.info(f"Результат замены лица: {result_path}")

    # Меняем текст на сообщении
    await call.message.edit_text(text.SAVE_IMAGE_PROGRESS_TEXT.format(image_index))

    # Сохраняем изображение
    image_index = int(image_index) - 1
    now = datetime.now().strftime("%Y-%m-%d")
    link = await saveFile(result_path, user_id, model_name, picture_folder_id, now)

    if not link:
        await call.message.answer(text.SAVE_FILE_ERROR_TEXT)
        return

    await state.update_data(image_url=link)

    # Получаем данные родительской папки
    folder = getFolderDataByID(picture_folder_id)
    parent_folder_id = folder['parents'][0]
    parent_folder = getFolderDataByID(parent_folder_id)

    logger.info(f"Данные папки по id {picture_folder_id}: {folder}")

    # Удаляем текущее сообщение
    await bot.delete_message(user_id, call.message.message_id)

    # Отправляем сообщение о сохранении изображения
    await call.message.answer(text.SAVE_IMAGES_SUCCESS_TEXT
    .format(link, model_name, parent_folder['webViewLink']), reply_markup=generateVideoKeyboard(model_name))

    # Удаляем отправленные изображения из чата
    try:    
        mediagroup_messages_ids = stateData[f"mediagroup_messages_ids_{model_name}"]
        chat_id = call.message.chat.id
        for message_id in mediagroup_messages_ids:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logger.error(f"Произошла ошибка при удалении изображений из чата: {e}")

    # Удаляем изображение с заменённым лицом
    os.remove(result_path)


# Обработка нажатия кнопки "📹 Сгенерировать видео"
async def start_generate_video(call: types.CallbackQuery, state: FSMContext):
    # Получаем название модели
    model_name = call.data.split("|")[1]

    # Получаем id пользователя и удаляем сообщение
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(user_id, message_id)

    # Удаляем видео из папки temp/videos, если оно есть
    stateData = await state.get_data()
    if "video_path" in stateData:
        os.remove(stateData["video_path"])

    # Отправляем сообщение для выбора видео-примеров
    await call.message.answer(text.SELECT_VIDEO_EXAMPLE_TEXT.format(model_name))

    # Получаем все видео-шаблоны с их промптами
    templates_examples = await getVideoExamplesData()

    # Выгружаем видео-примеры вместе с их промптами
    video_examples_messages_ids = []
    for index, value in templates_examples.items():
        video = types.FSInputFile(value["file_path"])
        video_example_message = await call.message.answer_video(
            video=video,
            caption=text.VIDEO_EXAMPLE_TEXT.format(model_name, value["prompt"]),
            reply_markup=videoExampleKeyboard(index, model_name)
        )
        video_examples_messages_ids.append(video_example_message.message_id)
        await state.update_data(video_examples_messages_ids=video_examples_messages_ids)


# Обработка нажатия кнопок под видео-примером
async def handle_video_example_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем индекс видео-примера и тип кнопки
    temp = call.data.split("|")
    index = int(temp[1])
    model_name = temp[2]
    button_type = temp[3]
    user_id = call.from_user.id

    # Получаем название модели и url изображения
    data = await state.get_data()
    image_url = data["image_url"]

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
    await state.update_data(video_example_file_path=video_example_file_path)

    # Удаляем сообщения с видео-примерами
    video_examples_messages_ids = data["video_examples_messages_ids"]
    for message_id in video_examples_messages_ids:
        try:
            await bot.delete_message(user_id, int(message_id))
        except Exception as e:
            logger.error(f"Произошла ошибка при удалении сообщения с id {message_id}: {e}")
            
    # Удаляем текущее сообщение
    try:
        await bot.delete_message(user_id, call.message.message_id)
    except Exception as e:
        logger.error(f"Произошла ошибка при удалении сообщения с id {call.message.message_id}: {e}")

    # Если кнопка "Написать промпт", то отправляем сообщение для ввода кастомного промпта
    if button_type == "write_prompt":
        await state.update_data(video_example_file_path=video_example_file_path)
        await state.update_data(video_example_index=index)
        await state.update_data(model_name=model_name)
        await call.message.answer(text.WRITE_PROMPT_FOR_VIDEO_TEXT.format(model_name))
        await state.set_state(UserState.write_prompt_for_video)
        return
    
    # Отправляем сообщение под генерацию видео
    message_for_delete = await call.message.answer(text.GENERATE_VIDEO_PROGRESS_TEXT.format(model_name))

    # Генерируем видео
    try:
        video_path = await generateVideo(video_example_prompt, image_url)
    except Exception as e:
        traceback.print_exc()
        await call.message.answer(text.GENERATE_VIDEO_ERROR_TEXT.format(e))
        logger.error(f"Произошла ошибка при генерации видео: {e}")
        return
    
    # Сохраняем видео в стейт
    await state.update_data(video_path=video_path)

    # Удаляем сообщение про генерацию видео
    await bot.delete_message(user_id, message_for_delete.message_id)

    # Отправляем видео
    video = types.FSInputFile(video_path)
    if button_type == "test":
        await call.message.answer_video(video=video, caption=text.GENERATE_TEST_VIDEO_SUCCESS_TEXT.format(model_name), 
        reply_markup=videoExampleKeyboard(index, model_name, False))

    elif button_type == "work":
        await call.message.answer_video(video=video, caption=text.GENERATE_VIDEO_SUCCESS_TEXT.format(model_name), 
        reply_markup=videoCorrectnessKeyboard(model_name))


# Хедлер для обработки ввода кастомного промпта для видео
async def write_prompt_for_video(message: types.Message, state: FSMContext):
    # Получаем данные
    prompt = message.text
    await state.update_data(prompt_for_video=prompt)
    data = await state.get_data()
    video_example_file_path = data["video_example_file_path"]
    index = data["video_example_index"]

    # Отправляем видео
    video = types.FSInputFile(video_example_file_path)
    await message.answer_video(video, 
    caption=text.WRITE_PROMPT_FOR_VIDEO_SUCCESS_TEXT.format(data["model_name"], prompt),
    reply_markup=videoExampleKeyboard(index, data["model_name"], with_write_prompt=False))


# Обработка нажатия на кнопки корректности видео
async def handle_video_correctness_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем тип кнопки
    temp = call.data.split("|")
    button_type = temp[1]
    model_name = temp[2]

    # Получаем данные
    data = await state.get_data()
    video_path = data["video_path"]
    user_id = call.from_user.id
    video_folder_id = data["video_folder_id"]
    now = datetime.now().strftime("%Y-%m-%d")

    if button_type == "correct":
        # Удаляем текущее сообщение
        await bot.delete_message(user_id, call.message.message_id)

        # Отправляем сообщение о начале сохранения видео
        message_for_edit = await call.message.answer(text.SAVE_VIDEO_PROGRESS_TEXT.format(model_name))

        # Сохраняем видео
        link = await saveFile(video_path, user_id, model_name, video_folder_id, now, False)

        if not link:
            await call.message.answer(text.SAVE_FILE_ERROR_TEXT)
            return
        
        # Получаем данные родительской папки
        folder = getFolderDataByID(video_folder_id)
        parent_folder_id = folder['parents'][0]
        parent_folder = getFolderDataByID(parent_folder_id)

        logger.info(f"Данные папки по id {video_folder_id}: {folder}")

        # Отправляем сообщение о сохранении видео
        await message_for_edit.edit_text(text.SAVE_VIDEO_SUCCESS_TEXT
        .format(link, model_name, parent_folder['webViewLink']))

        # Удаляем видео из папки temp/videos
        os.remove(video_path)


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

    router.callback_query.register(start_generate_video, lambda call: call.data.startswith("start_generate_video"))

    router.callback_query.register(handle_video_example_buttons, lambda call: call.data.startswith("generate_video"))

    router.message.register(write_prompt_for_video, StateFilter(UserState.write_prompt_for_video))

    router.callback_query.register(handle_video_correctness_buttons, 
    lambda call: call.data.startswith("video_correctness"))