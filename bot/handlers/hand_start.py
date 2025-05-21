from utils.handlers.generateImagesInHandler import generateImagesInHandler
from utils.generateImages.dataArray.getDataByModelName import getDataByModelName
from utils.generateImages.dataArray.getNextModel import getNextModel
from utils.generateImages.dataArray.getAllDataArrays import getAllDataArrays
from utils import retryOperation
from utils.generateImages.dataArray.getDataArrayBySettingNumber import getDataArrayBySettingNumber
from utils.videos.generateVideo import generateVideo
from utils.facefusion.facefusion_swap import facefusion_swap
from aiogram import types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from utils.videoExamples.getVideoExampleDataByIndex import getVideoExampleDataByIndex
from utils.saveImages.getFolderDataByID import getFolderDataByID
from utils.files.saveFile import saveFile
from utils.generateImages.generateImageBlock import generateImageBlock
from keyboards.user import keyboards
from utils import text
from states import UserState
from logger import logger
from InstanceBot import bot
import traceback
from utils.videoExamples.getVideoExamplesData import getVideoExamplesData
from InstanceBot import router
import os
from datetime import datetime
from aiogram.filters import Command
from utils.generateImages.dataArray.getModelNameIndex import getModelNameIndex
from utils.generateImages.upscaleImage import upscaleImage
from config import TEMP_FOLDER_PATH
from PIL import Image
from utils.generateImages.ImageTobase64 import imageToBase64
from utils.generateImages.base64ToImage import base64ToImage
import asyncio


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text.START_TEXT, reply_markup=keyboards.generationsTypeKeyboard()
    )


# Обработка выбора количества генераций
async def choose_generations_type(
    call: types.CallbackQuery, state: FSMContext
):
    generations_type = call.data.split("|")[1]
    await state.update_data(generations_type=generations_type)

    try:
        prompt_exist = bool(call.data.split("|")[2])
    except:
        prompt_exist = False
    
    await state.update_data(prompt_exist=prompt_exist)

    await call.message.edit_text(
        text.GET_GENERATIONS_SUCCESS_TEXT,
        reply_markup=keyboards.selectSettingKeyboard(),
    )


# Обработка выбора настройки
async def choose_setting(call: types.CallbackQuery, state: FSMContext):
    setting_number = call.data.split("|")[1]
    await state.update_data(setting_number=setting_number)
    data = await state.get_data()
    generations_type = data["generations_type"]
    prompt_exist = data["prompt_exist"]

    if generations_type == "test":
        if prompt_exist:
            prompt = data["prompt"]
            user_id = call.from_user.id
            is_test_generation = generations_type == "test"
            setting_number = setting_number

            # Удаляем сообщение с выбором настройки
            await bot.delete_message(user_id, call.message.message_id)

            await generateImagesInHandler(prompt, call.message, state, user_id, is_test_generation, setting_number)

            await state.update_data(prompt_exist=False)
        else:
            await call.message.edit_text(
                text.GET_SETTINGS_SUCCESS_TEXT
            )
            await state.set_state(UserState.write_prompt_for_images)

    elif generations_type == "work":
        await call.message.edit_text(
            text.CHOOSE_WRITE_PROMPT_TYPE_SUCCESS_TEXT,
            reply_markup=keyboards.writePromptTypeKeyboard()
        )


# Обработка выбора режима написания промпта
async def choose_writePrompt_type(call: types.CallbackQuery, state: FSMContext):
    # Получаем данные
    writePrompt_type = call.data.split("|")[1]
    await state.update_data(writePrompt_type=writePrompt_type)

    if writePrompt_type == "one":
        await call.message.edit_text(text.GET_ONE_PROMPT_GENERATION_SUCCESS_TEXT, reply_markup=keyboards.onePromptGenerationChooseTypeKeyboard())
    else:
        # Получаем данные
        stateData = await state.get_data()
        setting_number = stateData["setting_number"]

        if setting_number == "all":
            # Получаем все настройки
            dataArrays = getAllDataArrays()

            # Инициализируем начальные данные
            model_name = dataArrays[0][0]["model_name"]
            await state.update_data(current_setting_number_for_unique_prompt=1)
            await state.set_state(UserState.write_prompt_for_model)
        else:
            # Получаем данные по настройке
            dataArray = getDataArrayBySettingNumber(int(setting_number))
            model_name = dataArray[0]["model_name"]
            await state.update_data(current_setting_number_for_unique_prompt=int(setting_number))

        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

        await call.message.edit_text(text.WRITE_PROMPT_FOR_MODEL_START_TEXT.format(model_name, model_name_index))
        await state.update_data(current_model_for_unique_prompt=model_name)
        await state.set_state(UserState.write_prompt_for_model)


# Обработка выбора режима при генерации с одним промптом
async def chooseOnePromptGenerationType(call: types.CallbackQuery, state: FSMContext):
    one_prompt_generation_type = call.data.split("|")[1]

    if one_prompt_generation_type == "static":
        await call.message.edit_text(text.GET_STATIC_PROMPT_TYPE_SUCCESS_TEXT)
        await state.set_state(UserState.write_prompt_for_images)

    elif one_prompt_generation_type == "random":
        await call.message.edit_text(text.GET_RANDOM_PROMPT_TYPE_SUCCESS_TEXT, 
        reply_markup=keyboards.randomizerKeyboard([]))


# Обработка кнопок в меню рандомайзера
async def handle_randomizer_buttons(call: types.CallbackQuery, state: FSMContext):
    variable_name = call.data.split("|")[1]
    
    # Если была выбрана кнопка "✅ Добавить переменную"
    if variable_name == "add_variable":
        await call.message.edit_text(text.ADD_VARIABLE_FOR_RANDOMIZER_TEXT)
        await state.set_state(UserState.write_variable_for_randomizer)


# Обработка ввода переменных для рандомайзера
async def write_variable_for_randomizer(message: types.Message, state: FSMContext):
    # Получаем данные
    data = await state.get_data()
    variable_name = message.text

    # Если переменная ещё не добавлена в стейт, то добавляем её
    if "variable_names_for_randomizer" not in data:
        await state.update_data(variable_names_for_randomizer=[variable_name])
    else:
        data["variable_names_for_randomizer"].append(variable_name)
        await state.update_data(variable_names_for_randomizer=data["variable_names_for_randomizer"])

    await message.answer(text.WRITE_VARIABLE_FOR_RANDOMIZER_TEXT, 
    reply_markup=keyboards.stopInputValuesForVariableKeyboard())
    await state.set_state(UserState.write_value_for_variable_for_randomizer)


# Обработка ввода значения для переменной для рандомайзера
async def write_value_for_variable_for_randomizer(message: types.Message, state: FSMContext):
    # Получаем данные
    data = await state.get_data()
    all_variable_names = data["variable_names_for_randomizer"]
    variable_name = all_variable_names[-1]
    variable_name_values = f"randomizer_{variable_name}_values"

    # Если пользователь нажал на кнопку "🚫 Остановить ввод значений", то прекращаем ввод значений для переменной
    if message.text == "🚫 Остановить ввод значений":
        await message.answer(text.RANDOMIZER_MENU_TEXT, 
        reply_markup=keyboards.randomizerKeyboard(all_variable_names))
        return
    
    # Получаем значение в ином случае
    value = message.text
    
    # Если переменной ещё нет в стейте, то создаём её
    if variable_name_values not in data:
        await state.update_data(**{variable_name_values: [value]})
    else: # Если переменная уже есть в стейте, то добавляем значение в список
        data[variable_name_values].append(value)
        await state.update_data(**{variable_name_values: data[variable_name_values]})

    await message.answer(text.WRITE_VALUE_FOR_VARIABLE_FOR_RANDOMIZER_TEXT.format(variable_name))
    await state.set_state(UserState.write_value_for_variable_for_randomizer)


# Обработка ввода промпта
async def write_prompt(message: types.Message, state: FSMContext):
    prompt = message.text
    user_id = message.from_user.id
    data = await state.get_data()
    is_test_generation = data["generations_type"] == "test"
    setting_number = data["setting_number"]
    await state.update_data(prompt=prompt)

    await generateImagesInHandler(prompt, message, state, user_id, is_test_generation, setting_number)
            

# Обработка ввода промпта для конкретной модели
async def write_prompt_for_model(message: types.Message, state: FSMContext):
    # Получаем данные
    data = await state.get_data()
    prompt = message.text
    model_name = data["current_model_for_unique_prompt"]
    setting_number = data["setting_number"]
    user_id = message.from_user.id

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение о начале генерации
    message_for_edit = await message.answer(text.GENERATE_IMAGE_PROGRESS_TEXT.format(model_name, model_name_index))

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    # Прибавляем к каждому элементу массива корневой промпт
    data["json"]['input']['prompt'] += " " + prompt

    # Генерируем изображения
    await generateImageBlock(data["json"], model_name, message_for_edit, state, user_id, setting_number, False)
    
    # Получаем следующую модель
    next_model = await getNextModel(model_name, setting_number, state)

    logger.info(f"Следующая модель: {next_model}")

    # Если следующая модель не найдена, то завершаем генерацию
    if not next_model:
        await message.answer(text.GENERATE_IMAGE_SUCCESS_TEXT)
        await state.clear()
        return

    # Получаем индекс следующей модели
    next_model_index = getModelNameIndex(next_model)

    # Просим пользователя отправить промпт для следующей модели
    await message.answer(text.WRITE_PROMPT_FOR_MODEL_TEXT.format(next_model, next_model_index), 
    reply_markup=keyboards.confirmWriteUniquePromptForNextModelKeyboard())
    await state.update_data(current_model_for_unique_prompt=next_model)


# Обработка нажатия кнопки "✅ Написать промпт" для подтверждения написания уникального промпта для следующей модели
async def confirm_write_unique_prompt_for_next_model(call: types.CallbackQuery, state: FSMContext):
    # Получаем данные
    data = await state.get_data()
    next_model = data["current_model_for_unique_prompt"]

    # Получаем индекс следующей модели
    next_model_index = getModelNameIndex(next_model)

    # Отправляем сообщение для ввода промпта
    await call.message.edit_text(text.WRITE_UNIQUE_PROMPT_FOR_MODEL_TEXT.format(next_model, next_model_index))
    await state.set_state(UserState.write_prompt_for_model)


# Обработка выбора изображения
async def select_image(call: types.CallbackQuery, state: FSMContext):
    # Получаем id пользователя
    user_id = call.from_user.id

    # Получаем индекс работы и индекс изображения
    model_name = call.data.split("|")[1]
    setting_number = call.data.split("|")[2]
    image_index = call.data.split("|")[3]

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Если индекс изображения равен "regenerate", то перегенерируем изображение
    if image_index == "regenerate":
        stateData = await state.get_data()
        is_test_generation = stateData["generations_type"] == "test"

        # Отправляем сообщение о перегенерации изображения
        await call.message.edit_text(text.REGENERATE_IMAGE_TEXT.format(model_name, model_name_index))

        # Получаем данные генерации по названию модели
        data = await getDataByModelName(model_name)
        return await generateImageBlock(data["json"], model_name, call.message, state, user_id, setting_number, is_test_generation, False)
    
    # Получаем данные генерации по названию модели
    dataArray = getDataArrayBySettingNumber(int(setting_number))
    data = next((data for data in dataArray if data["model_name"] == model_name), None)
    picture_folder_id = data["picture_folder_id"]
    video_folder_id = data["video_folder_id"]

    # Сохраняем название модели и id папки для видео
    await state.update_data(model_name=model_name)
    await state.update_data(video_folder_id=video_folder_id)

    # Меняем текст на сообщении о начале upscale
    await call.message.edit_text(text.UPSCALE_IMAGE_PROGRESS_TEXT.format(image_index, model_name, model_name_index))

    # Получаем само изображение по пути
    image_path = f"{TEMP_FOLDER_PATH}/{model_name}_{user_id}/{image_index}.jpg"
    image = Image.open(image_path)
    image_base64 = imageToBase64(image)

    # Получаем негатив промпт
    negative_prompt = data["json"]["input"]["negative_prompt"]
    
    # Получаем базовую модель   
    base_model = data["json"]["input"]["base_model_name"]
    
    # Делаем upscale изображения
    images_output_base64 = await upscaleImage(image_base64, negative_prompt, base_model)

    # Сохраняем изображения по этому же пути
    await base64ToImage(images_output_base64, model_name, int(image_index) - 1, user_id, False)

    # Меняем текст на сообщении об очереди на замену лица
    await call.message.edit_text(text.FACE_SWAP_WAIT_TEXT.format(model_name, model_name_index))

    # Заменяем лицо на исходном изображении, которое сгенерировалось, на лицо с изображения модели
    faceswap_target_path = f"images/temp/{model_name}_{user_id}/{image_index}.jpg"
    faceswap_source_path = f"images/faceswap/{model_name}.jpg"
    logger.info(f"Путь к исходному изображению для замены лица: {faceswap_target_path}")
    logger.info(f"Путь к целевому изображению для замены лица: {faceswap_source_path}")

    # Если стейта для сохранения моделей и их изображений для faceswap ещё нет, то создаём его
    stateData = await state.get_data()
    if "faceswap_generate_models" not in stateData:
        await state.update_data(faceswap_generate_models=[model_name])
    else:
        # Добавляем в стейт путь к изображению для faceswap
        stateData["faceswap_generate_models"].append(model_name)
        await state.update_data(faceswap_generate_models=stateData["faceswap_generate_models"])

    # Запускаем цикл, что пока очередь генераций не освободится, то ответ не будет выдан и генерацию не начинаем
    while True:
        stateData = await state.get_data()
        faceswap_generate_models = stateData["faceswap_generate_models"]

        logger.info(f"Список генераций для замены лица: {faceswap_generate_models}")

        # Если в списке генераций настала очередь этой модели, то запускаем генерацию
        if model_name == faceswap_generate_models[0]:
            await call.message.edit_text(text.FACE_SWAP_PROGRESS_TEXT.format(image_index, model_name, model_name_index))
            
            try:
                result_path = await retryOperation(facefusion_swap, 10, 1.5, faceswap_source_path, faceswap_target_path)
            except Exception as e:
                result_path = None
                logger.error(f"Произошла ошибка при замене лица: {e}")
                await call.message.answer(text.FACE_SWAP_ERROR_TEXT.format(model_name, model_name_index))
                break

            break

        await asyncio.sleep(10)

    # После генерации удаляем модель из стейта
    stateData = await state.get_data()
    stateData["faceswap_generate_models"].remove(model_name)
    await state.update_data(faceswap_models=stateData["faceswap_generate_models"])

    # Если результат замены лица не найден, то завершаем генерацию
    if not result_path:
        return

    logger.info(f"Результат замены лица: {result_path}")

    # Меняем текст на сообщении
    await call.message.edit_text(text.SAVE_IMAGE_PROGRESS_TEXT.format(image_index, model_name, model_name_index))

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
    .format(link, model_name, parent_folder['webViewLink'], model_name_index), reply_markup=keyboards.generateVideoKeyboard(model_name))

    # Удаляем отправленные изображения из чата
    stateData = await state.get_data()
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

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение для выбора видео-примеров
    select_video_example_message = await call.message.answer(text.SELECT_VIDEO_EXAMPLE_TEXT.format(model_name, model_name_index))

    await state.update_data(select_video_example_message_id=select_video_example_message.message_id)

    # Получаем все видео-шаблоны с их промптами
    templates_examples = await getVideoExamplesData()

    # Выгружаем видео-примеры вместе с их промптами
    video_examples_messages_ids = []
    for index, value in templates_examples.items():
        video_example_message = await call.message.answer_video(
            video=value["file_id"],
            caption=text.VIDEO_EXAMPLE_TEXT.format(model_name, model_name_index, value["prompt"]),
            reply_markup=keyboards.videoExampleKeyboard(index, model_name)
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

    # Удаляем сообщение с выбором видео-примера
    try:
        await bot.delete_message(user_id, int(data["select_video_example_message_id"]))
    except Exception as e:
        logger.error(f"Произошла ошибка при удалении сообщения с id {data['select_video_example_message_id']}: {e}")

    # Получаем данные видео-примера по его индексу
    video_example_data = await getVideoExampleDataByIndex(index)

    # Получаем кастомный промпт, если он есть, а если нет, то берем промпт из видео-примера 
    if "prompt_for_video" in data:
        custom_prompt = data["prompt_for_video"]
    else:
        custom_prompt = None
    video_example_prompt = custom_prompt if custom_prompt else video_example_data["prompt"]

    # Получаем путь к видео-примеру
    video_example_file_id = video_example_data["file_id"]
    await state.update_data(video_example_file_id=video_example_file_id)

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

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Если кнопка "Написать промпт", то отправляем сообщение для ввода кастомного промпта
    if button_type == "write_prompt":
        await state.update_data(video_example_file_id=video_example_file_id)
        await state.update_data(video_example_index=index)
        await state.update_data(model_name=model_name)
        await call.message.answer(text.WRITE_PROMPT_FOR_VIDEO_TEXT.format(model_name, model_name_index))
        await state.set_state(UserState.write_prompt_for_video)
        return
    
    # Отправляем сообщение под генерацию видео
    message_for_delete = await call.message.answer(text.GENERATE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index))

    # Генерируем видео
    try:
        video_path = await retryOperation(generateVideo, 10, 1.5, video_example_prompt, image_url)
    except Exception as e:
        # Удаляем сообщение про генерацию видео
        await bot.delete_message(user_id, message_for_delete.message_id)

        # Отправляем сообщение об ошибке
        traceback.print_exc()
        await call.message.answer(text.GENERATE_VIDEO_ERROR_TEXT.format(model_name, e))
        logger.error(f"Произошла ошибка при генерации видео для модели {model_name}: {e}")
        return
    
    # Сохраняем видео в стейт
    await state.update_data(video_path=video_path)

    # Удаляем сообщение про генерацию видео
    await bot.delete_message(user_id, message_for_delete.message_id)

    # Отправляем видео
    video = types.FSInputFile(video_path)
    if button_type == "test":
        await call.message.answer_video(video=video, caption=text.GENERATE_TEST_VIDEO_SUCCESS_TEXT.format(model_name), 
        reply_markup=keyboards.videoExampleKeyboard(index, model_name, False))

    elif button_type == "work":
        await call.message.answer_video(video=video, caption=text.GENERATE_VIDEO_SUCCESS_TEXT.format(model_name, model_name_index), 
        reply_markup=keyboards.videoCorrectnessKeyboard(model_name))


# Хедлер для обработки ввода кастомного промпта для видео
async def write_prompt_for_video(message: types.Message, state: FSMContext):
    # Получаем данные
    prompt = message.text
    await state.update_data(prompt_for_video=prompt)
    data = await state.get_data()
    video_example_file_id = data["video_example_file_id"]
    index = data["video_example_index"]

    # Отправляем видео
    await message.answer_video(video_example_file_id, 
    caption=text.WRITE_PROMPT_FOR_VIDEO_SUCCESS_TEXT.format(data["model_name"], prompt),
    reply_markup=keyboards.videoExampleKeyboard(index, data["model_name"], with_write_prompt=False))


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
        message_for_edit = await call.message.answer(text.SAVE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index))

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

        # Удаляем сообщение про генерацию видео
        await bot.delete_message(user_id, message_for_edit.message_id)

        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

        # Отправляем сообщение о сохранении видео
        await message_for_edit.answer(text.SAVE_VIDEO_SUCCESS_TEXT
        .format(link, model_name, parent_folder['webViewLink'], model_name_index))

        # Удаляем видео из папки temp/videos
        os.remove(video_path)


# Обработка команды /stop   
async def stop_generation(message: types.Message, state: FSMContext):
    await state.update_data(stop_generation=True)
    await message.answer(text.STOP_GENERATION_TEXT)


# DEV: Функция для получения file_id видео В Telegram
# async def get_file_id(message: types.Message):
#     await message.answer(message.video.file_id)


# Добавление обработчиков
def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart())

    router.message.register(stop_generation, Command("stop"))

    router.callback_query.register(
        choose_generations_type,
        lambda call: call.data.startswith("generations_type"),
    )

    router.callback_query.register(
        choose_setting, lambda call: call.data.startswith("select_setting")
    )

    router.callback_query.register(
        choose_writePrompt_type, lambda call: call.data.startswith("write_prompt_type")
    )

    router.callback_query.register(
        chooseOnePromptGenerationType, lambda call: call.data.startswith("one_prompt_generation_type")
    )

    router.callback_query.register(handle_randomizer_buttons, lambda call: call.data.startswith("randomizer"))

    router.message.register(write_variable_for_randomizer, StateFilter(UserState.write_variable_for_randomizer))

    router.message.register(write_value_for_variable_for_randomizer, StateFilter(UserState.write_value_for_variable_for_randomizer))

    router.message.register(write_prompt, StateFilter(UserState.write_prompt_for_images))

    router.message.register(write_prompt_for_model, StateFilter(UserState.write_prompt_for_model))

    router.callback_query.register(confirm_write_unique_prompt_for_next_model, lambda call: call.data.startswith("confirm_write_unique_prompt_for_next_model"))

    router.callback_query.register(select_image, lambda call: call.data.startswith("select_image"))

    router.callback_query.register(start_generate_video, lambda call: call.data.startswith("start_generate_video"))

    router.callback_query.register(handle_video_example_buttons, lambda call: call.data.startswith("generate_video"))

    router.message.register(write_prompt_for_video, StateFilter(UserState.write_prompt_for_video))

    router.callback_query.register(handle_video_correctness_buttons, 
    lambda call: call.data.startswith("video_correctness"))

    # DEV: Получение file_id видео
    # router.message.register(get_file_id)