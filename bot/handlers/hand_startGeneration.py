from utils.handlers.generateImagesInHandler import generateImagesInHandler
from utils.generateImages.dataArray.getDataByModelName import getDataByModelName
from utils.generateImages.dataArray.getNextModel import getNextModel
from utils.generateImages.dataArray.getAllDataArrays import getAllDataArrays
from utils import retryOperation
from utils.generateImages.dataArray.getDataArrayBySettingNumber import getDataArrayBySettingNumber
from utils.facefusion.facefusion_swap import facefusion_swap
from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from utils.saveImages.getFolderDataByID import getFolderDataByID
from utils.files.saveFile import saveFile
from utils.generateImages.generateImageBlock import generateImageBlock
from keyboards import start_generation_keyboards, randomizer_keyboards, video_generation_keyboards
from utils import text
from states.UserState import StartGenerationState
from logger import logger
from InstanceBot import bot
from InstanceBot import router
import os
from datetime import datetime
from utils.generateImages.dataArray.getModelNameIndex import getModelNameIndex
from utils.generateImages.upscaleImage import upscaleImage
from config import TEMP_FOLDER_PATH
from PIL import Image
from utils.generateImages.ImageTobase64 import imageToBase64
from utils.generateImages.base64ToImage import base64ToImage
import asyncio
from utils.handlers.editMessageOrAnswer import editMessageOrAnswer
from utils.generateImages.dataArray.getSettingNumberByModelName import getSettingNumberByModelName
import traceback


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

    await editMessageOrAnswer(
        call,
        text.GET_GENERATIONS_SUCCESS_TEXT,
        reply_markup=start_generation_keyboards.selectSettingKeyboard(is_test_generation=generations_type == "test"),
    )


# Обработка выбора настройки
async def choose_setting(call: types.CallbackQuery, state: FSMContext):
    # Если выбрана конкретная модель, то просим ввести название модели
    if call.data == 'select_setting|specific_model':
        await editMessageOrAnswer(
            call,
            text.WRITE_MODELS_NAME_TEXT
        )
        # Очищаем стейт
        await state.set_state(StartGenerationState.write_model_name_for_generation)
        return 

    # Если выбрана другая настройка, то продолжаем генерацию
    setting_number = call.data.split("|")[1]
    await state.update_data(setting_number=setting_number)
    data = await state.get_data()
    generations_type = data["generations_type"]
    prompt_exist = data["prompt_exist"]
    
    # Если выбрана настройка для теста, то продолжаем генерацию в тестовом режиме
    if generations_type == "test":
        if prompt_exist:
            prompt = data["prompt_for_images"]
            user_id = call.from_user.id
            is_test_generation = generations_type == "test"
            setting_number = setting_number

            # Удаляем сообщение с выбором настройки
            await bot.delete_message(user_id, call.message.message_id)

            await generateImagesInHandler(prompt, call.message, state, user_id, is_test_generation, setting_number)

            await state.update_data(prompt_exist=False)
        else:
            await editMessageOrAnswer(
        call,
                text.GET_SETTINGS_SUCCESS_TEXT
            )
            await state.set_state(StartGenerationState.write_prompt_for_images)

    # Если выбрана настройка для работы, то продолжаем генерацию в рабочем режиме
    elif generations_type == "work":
        await editMessageOrAnswer(
        call,
            text.CHOOSE_WRITE_PROMPT_TYPE_SUCCESS_TEXT,
            reply_markup=start_generation_keyboards.writePromptTypeKeyboard()
        )


# Обработка выбора режима написания промпта
async def choose_writePrompt_type(call: types.CallbackQuery, state: FSMContext):
    # Получаем данные
    writePrompt_type = call.data.split("|")[1]
    await state.update_data(writePrompt_type=writePrompt_type)

    if writePrompt_type == "one":
        await editMessageOrAnswer(
        call,text.GET_ONE_PROMPT_GENERATION_SUCCESS_TEXT, 
        reply_markup=start_generation_keyboards.onePromptGenerationChooseTypeKeyboard())
        
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
            await state.set_state(StartGenerationState.write_prompt_for_model)
        else:
            # Получаем данные по настройке
            dataArray = getDataArrayBySettingNumber(int(setting_number))
            model_name = dataArray[0]["model_name"]
            await state.update_data(current_setting_number_for_unique_prompt=int(setting_number))

        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

        await editMessageOrAnswer(
        call,text.WRITE_PROMPT_FOR_MODEL_START_TEXT.format(model_name, model_name_index))
        await state.update_data(current_model_for_unique_prompt=model_name)
        await state.set_state(StartGenerationState.write_prompt_for_model)


# Обработка выбора режима при генерации с одним промптом
async def chooseOnePromptGenerationType(call: types.CallbackQuery, state: FSMContext):
    one_prompt_generation_type = call.data.split("|")[1]

    if one_prompt_generation_type == "static":
        await editMessageOrAnswer(
        call,text.GET_STATIC_PROMPT_TYPE_SUCCESS_TEXT)
        await state.set_state(StartGenerationState.write_prompt_for_images)

    elif one_prompt_generation_type == "random":
        # Очищаем все данные, которые используются в рандомайзере
        await state.update_data(variable_names_for_randomizer=[])
        await state.update_data(variable_name_values=[])
        await editMessageOrAnswer(
        call,text.GET_RANDOM_PROMPT_TYPE_SUCCESS_TEXT, 
        reply_markup=randomizer_keyboards.randomizerKeyboard([]))


# Обработка ввода промпта
async def write_prompt(message: types.Message, state: FSMContext):
    # Получаем данные
    prompt = message.text
    user_id = message.from_user.id
    data = await state.get_data()
    is_test_generation = data["generations_type"] == "test"
    await state.update_data(prompt_for_images=prompt)

    await state.set_state(None)

    # Если в стейте есть номер настройки, то используем его, иначе получаем номер настройки по названию модели
    if "setting_number" in data:
        setting_number = data["setting_number"]

        # Генерируем изображения
        await generateImagesInHandler(prompt, message, state, user_id, is_test_generation, setting_number)
    else:
        model_names = data["model_names_for_generation"]
        logger.info(f"Список моделей для генерации: {model_names}")

        # Генерируем изображения
        await generateImagesInHandler(prompt, message, state, user_id, is_test_generation, None)


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

    await state.set_state(None)
    # Просим пользователя отправить промпт для следующей модели
    await message.answer(text.WRITE_PROMPT_FOR_MODEL_TEXT.format(next_model, next_model_index), 
    reply_markup=start_generation_keyboards.confirmWriteUniquePromptForNextModelKeyboard())
    await state.update_data(current_model_for_unique_prompt=next_model)


# Обработка нажатия кнопки "✅ Написать промпт" для подтверждения написания уникального промпта для следующей модели
async def confirm_write_unique_prompt_for_next_model(call: types.CallbackQuery, state: FSMContext):
    # Получаем данные
    data = await state.get_data()
    next_model = data["current_model_for_unique_prompt"]

    # Получаем индекс следующей модели
    next_model_index = getModelNameIndex(next_model)

    # Отправляем сообщение для ввода промпта
    await editMessageOrAnswer(
        call,text.WRITE_UNIQUE_PROMPT_FOR_MODEL_TEXT.format(next_model, next_model_index))
    await state.set_state(StartGenerationState.write_prompt_for_model)


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
        await editMessageOrAnswer(
        call,text.REGENERATE_IMAGE_TEXT.format(model_name, model_name_index))

        # Получаем данные генерации по названию модели
        data = await getDataByModelName(model_name)

        # Прибавляем к каждому элементу массива корневой промпт
        data["json"]['input']['prompt'] += " " + stateData["prompt_for_images"]

        return await generateImageBlock(data["json"], model_name, call.message, state, user_id, setting_number, is_test_generation, False)
    
    # Получаем данные генерации по названию модели
    dataArray = getDataArrayBySettingNumber(int(setting_number))
    # Пытаемся найти данные в текущем массиве
    data = next((data for data in dataArray if data["model_name"] == model_name), None)
    
    # Если данные не найдены, ищем во всех доступных массивах
    if data is None:
        all_data_arrays = getAllDataArrays()
        for arr in all_data_arrays:
            data = next((d for d in arr if d["model_name"] == model_name), None)
            if data is not None:
                break
    picture_folder_id = data["picture_folder_id"]
    video_folder_id = data["video_folder_id"]

    # Сохраняем название модели и id папки для видео
    await state.update_data(model_name=model_name)
    await state.update_data(video_folder_id=video_folder_id)

    # Меняем текст на сообщении о начале upscale
    await editMessageOrAnswer(
        call,text.UPSCALE_IMAGE_PROGRESS_TEXT.format(image_index, model_name, model_name_index))

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
    await editMessageOrAnswer(
        call,text.FACE_SWAP_WAIT_TEXT.format(model_name, model_name_index))

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
            await editMessageOrAnswer(
        call,text.FACE_SWAP_PROGRESS_TEXT.format(image_index, model_name, model_name_index))
            
            try:
                result_path = await retryOperation(facefusion_swap, 10, 1.5, faceswap_source_path, faceswap_target_path)
            except Exception as e:
                result_path = None
                logger.error(f"Произошла ошибка при замене лица: {e}")
                stateData["faceswap_generate_models"].remove(model_name)
                await state.update_data(faceswap_generate_models=stateData["faceswap_generate_models"])
                try:
                    await editMessageOrAnswer(
                    call,text.FACE_SWAP_ERROR_TEXT.format(model_name, model_name_index))
                except Exception as e:
                    logger.error(f"Произошла ошибка при отправке сообщения об ошибке: {e}")
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
    await editMessageOrAnswer(
        call,text.SAVE_IMAGE_PROGRESS_TEXT.format(image_index, model_name, model_name_index))

    # Сохраняем изображение
    image_index = int(image_index) - 1
    now = datetime.now().strftime("%Y-%m-%d")
    link = await saveFile(result_path, user_id, model_name, picture_folder_id, now)

    if not link:
        traceback.print_exc()
        await editMessageOrAnswer(
        call,text.SAVE_FILE_ERROR_TEXT.format(model_name, model_name_index))
        return

    dataForUpdate = {f"{model_name}": link}
    if "images_urls" not in stateData:
        await state.update_data(images_urls=dataForUpdate)
    else:
        stateData["images_urls"][model_name] = link
        await state.update_data(images_urls=stateData["images_urls"])

    # Получаем данные родительской папки
    folder = getFolderDataByID(picture_folder_id)
    parent_folder_id = folder['parents'][0]
    parent_folder = getFolderDataByID(parent_folder_id)

    logger.info(f"Данные папки по id {picture_folder_id}: {folder}")

    # Удаляем текущее сообщение
    await bot.delete_message(user_id, call.message.message_id)

    # Отправляем сообщение о сохранении изображения
    await editMessageOrAnswer(
        call,text.SAVE_IMAGES_SUCCESS_TEXT
    .format(link, model_name, parent_folder['webViewLink'], model_name_index), 
    reply_markup=video_generation_keyboards.generateVideoKeyboard(model_name))

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


# Обработка ввода названия модели для генерации
async def write_model_name_for_generation(message: types.Message, state: FSMContext):
    # Если в сообщении есть запятые, то записываем массив моделей в стейт
    model_names = message.text.split(",")
    
    # Если запятых нет, то записываем одну модель в стейт
    if len(model_names) == 1:
        model_names = [message.text]
    
    # Удаляем пробелы из названий моделей
    model_names = [model_name.strip() for model_name in model_names]
    
    # Проверяем, существует ли такие модели
    for model_name in model_names:
        # Если такой модели не существует, то просим ввести другое название
        if not await getDataByModelName(model_name):
            await message.answer(text.MODEL_NOT_FOUND_TEXT.format(model_name))
            return
        
    await state.update_data(model_names_for_generation=model_names)

    await state.set_state(None)
    await message.answer(text.GET_MODEL_NAME_SUCCESS_TEXT if len(model_names) == 1 else text.GET_MODEL_NAMES_SUCCESS_TEXT)
    await state.set_state(StartGenerationState.write_prompt_for_images)


# Добавление обработчиков
def hand_add():
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

    router.message.register(write_prompt, StateFilter(StartGenerationState.write_prompt_for_images))

    router.message.register(write_prompt_for_model, StateFilter(StartGenerationState.write_prompt_for_model))

    router.callback_query.register(confirm_write_unique_prompt_for_next_model, lambda call: call.data.startswith("confirm_write_unique_prompt_for_next_model"))

    router.callback_query.register(select_image, lambda call: call.data.startswith("select_image"))

    router.message.register(write_model_name_for_generation, StateFilter(StartGenerationState.write_model_name_for_generation))