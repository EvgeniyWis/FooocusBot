from datetime import datetime
from utils.googleDrive.folders import getFolderDataByID
from utils.googleDrive.files import saveFile
from utils.handlers import appendDataToStateArray, sendMessageForImageSaving, generateImagesInHandler, editMessageOrAnswer, waitForImageBlocksGeneration, regenerateImage
from utils import text
from utils.generateImages.dataArray import getDataByModelName, getNextModel, getDataArrayBySettingNumber, getAllDataArrays, getModelNameIndex, getSettingNumberByModelName
from utils.generateImages import generateImageBlock
from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards import start_generation_keyboards, randomizer_keyboards, video_generation_keyboards
from states.UserState import StartGenerationState
from logger import logger
from InstanceBot import bot, router
from config import TEMP_FOLDER_PATH
import asyncio

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
            text.WRITE_MODEL_NAME_TEXT
        )
        await state.update_data(specific_model=True)
        await state.set_state(StartGenerationState.write_model_name_for_generation)
        return 

    # Если выбрана другая настройка, то продолжаем генерацию
    setting_number = call.data.split("|")[1]
    await state.update_data(setting_number=setting_number)
    data = await state.get_data()
    generations_type = data["generations_type"]
    prompt_exist = data["prompt_exist"]
    await state.update_data(specific_model=False)
    
    # Если выбрана настройка для теста, то продолжаем генерацию в тестовом режиме
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

    # Если в стейте есть номер настройки, то используем его, иначе получаем номер настройки по названию модели
    if "setting_number" in data:
        setting_number = data["setting_number"]
    else:
        model_name = data["model_name_for_generation"]
        setting_number = getSettingNumberByModelName(model_name)

    await state.update_data(prompt=prompt)

    # Генерируем изображения
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
    
    # Если это режим генерации для конкретной модели, то не ждём пока появится следующий блок изображений в очереди
    stateData = await state.get_data()
    next_model_name = False
    
    if not stateData["specific_model"]:
        # Отправляем следующее изображение (ждём пока появится следующий блок изображений в очереди и отправляем его)
        next_model_name = asyncio.create_task(waitForImageBlocksGeneration(call.message, state))

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Если индекс изображения равен "regenerate", то перегенерируем изображение
    if image_index == "regenerate":
        return await regenerateImage(model_name, call, state, setting_number)
    
    try:
        # Добавляем в стейт то, сколько отправленных изображений
        stateData = await state.get_data()
        stateData["will_be_sent_generated_images_count"] += 1
        await state.update_data(will_be_sent_generated_images_count=stateData["will_be_sent_generated_images_count"])

        # Получаем данные генерации по названию модели
        dataArray = getDataArrayBySettingNumber(int(setting_number))
        data = next((data for data in dataArray if data["model_name"] == model_name), None)
        video_folder_id = data["video_folder_id"]

        # Сохраняем название модели и id папки для видео
        await state.update_data(model_name=model_name)
        await state.update_data(video_folder_id=video_folder_id)

        # # Меняем текст на сообщении о начале upscale
        # await editMessageOrAnswer(
        #     call,text.UPSCALE_IMAGE_PROGRESS_TEXT.format(image_index, model_name, model_name_index))

        # # Получаем само изображение по пути
        # image_path = f"{TEMP_FOLDER_PATH}/{model_name}_{user_id}/{image_index}.jpg"
        # image = Image.open(image_path)
        # image_base64 = imageToBase64(image)

        # # Получаем негатив промпт
        # negative_prompt = data["json"]["input"]["negative_prompt"]
        
        # # Получаем базовую модель   
        # base_model = data["json"]["input"]["base_model_name"]
        
        # # Делаем upscale изображения
        # images_output_base64 = await upscaleImage(image_base64, negative_prompt, base_model)

        # # Сохраняем изображения по этому же пути
        # await base64ToImage(images_output_base64, model_name, int(image_index) - 1, user_id, False)

        # # Меняем текст на сообщении об очереди на замену лица
        # await editMessageOrAnswer(
        #     call,text.FACE_SWAP_WAIT_TEXT.format(model_name, model_name_index))

        # # Заменяем лицо на исходном изображении, которое сгенерировалось, на лицо с изображения модели
        # faceswap_target_path = f"images/temp/{model_name}_{user_id}/{image_index}.jpg"
        # faceswap_source_path = f"images/faceswap/{model_name}.jpg"
        # logger.info(f"Путь к исходному изображению для замены лица: {faceswap_target_path}")
        # logger.info(f"Путь к целевому изображению для замены лица: {faceswap_source_path}")

        # # Добавляем в стейт путь к изображению для faceswap
        # await appendDataToStateArray(state, "faceswap_generate_models", model_name)

        # # Запускаем цикл, что пока очередь генераций не освободится, то ответ не будет выдан и генерацию не начинаем
        # while True:
        #     stateData = await state.get_data()
        #     faceswap_generate_models = stateData["faceswap_generate_models"]

        #     logger.info(f"Список генераций для замены лица: {faceswap_generate_models}")

        #     # Если в списке генераций настала очередь этой модели, то запускаем генерацию
        #     if model_name == faceswap_generate_models[0]:
        #         await editMessageOrAnswer(
        #     call,text.FACE_SWAP_PROGRESS_TEXT.format(image_index, model_name, model_name_index))
                
        #         try:
        #             result_path = await retryOperation(facefusion_swap, 10, 1.5, faceswap_source_path, faceswap_target_path)
        #         except Exception as e:
        #             result_path = None
        #             logger.error(f"Произошла ошибка при замене лица: {e}")
        #             await editMessageOrAnswer(
        #     call,text.FACE_SWAP_ERROR_TEXT.format(model_name, model_name_index))
        #             break

        #         break

        #     await asyncio.sleep(10)

        # # После генерации удаляем модель из стейта
        # stateData = await state.get_data()
        # stateData["faceswap_generate_models"].remove(model_name)
        # await state.update_data(faceswap_models=stateData["faceswap_generate_models"])

        # # Если результат замены лица не найден, то завершаем генерацию
        # if not result_path:
        #     return

        # logger.info(f"Результат замены лица: {result_path}")

        # Добавляем result_path в стейт
        # TODO: удалить потом этот result path и раскомментировать нормальный
        result_path = f"FocuuusBot/bot/assets/reference_images/abrilberries.jpeg"
        updateData = {f"{model_name}": result_path}
        await appendDataToStateArray(state, "generated_images", updateData)

        stateData = await state.get_data()
        logger.info(f"Список сгенерируемых изображений для сохранения: {stateData["generated_images"]}")

        # Меняем текст на сообщении
        await editMessageOrAnswer(
            call, text.FACE_SWAP_SUCCESS_TEXT.format(model_name, model_name_index))  

        # Добавляем в стейт то, сколько отправленных изображений
        stateData["finally_sent_generated_images_count"] += 1
        await state.update_data(finally_sent_generated_images_count=stateData["finally_sent_generated_images_count"])
        
    except Exception as e:
        logger.error(f"Произошла ошибка при генерации изображения: {e}")
        await editMessageOrAnswer(
            call, text.GENERATE_IMAGE_ERROR_TEXT.format(model_name, e))
        
    finally:
        if next_model_name and not stateData["specific_model"]:
            # Удаляем модель из очереди генерации
            stateData = await state.get_data()
            next_model_name = await next_model_name
            
            if not next_model_name:
                return
            
            logger.info(f"Удаляем модель из очереди генерации: {next_model_name} из списка: {stateData['models_for_generation_queue']}")
            stateData["models_for_generation_queue"].remove(next_model_name)
            await state.update_data(models_for_generation_queue=stateData["models_for_generation_queue"])


# Обработка нажатия кнопки "💾 Этап сохранения изображений"
async def save_images(call: types.CallbackQuery, state: FSMContext):
    await sendMessageForImageSaving(call, state)
    

# Обработка нажатия кнопок для сохранения изображения
async def save_image(call: types.CallbackQuery, state: FSMContext):
    # Получаем данные
    temp = call.data.split("|")
    model_name = temp[1]

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)
    
    # Получаем id пользователя
    user_id = call.from_user.id
    
    # Меняем текст на сообщении
    await editMessageOrAnswer(
        call,text.SAVE_IMAGE_PROGRESS_TEXT.format(model_name, model_name_index))
    
    # Получаем название модели, которая стоит первой в очереди
    stateData = await state.get_data()
    model_data = stateData["generated_images"][0]
    model_name = list(model_data.keys())[0]
    result_path = model_data[model_name]

    # Удаляем изображение из очереди
    stateData["generated_images"].pop(0)
    await state.update_data(generated_images=stateData["generated_images"])

    # Выдаём следующую модель
    await sendMessageForImageSaving(call, state)

    # Получаем данные модели
    model_data = await getDataByModelName(model_name)

    # Сохраняем изображение
    now = datetime.now().strftime("%Y-%m-%d")
    link = await saveFile(result_path, user_id, model_name, model_data["picture_folder_id"], now)

    if not link:
        await editMessageOrAnswer(
        call,text.SAVE_FILE_ERROR_TEXT)
        return

    # Делаем ссылку корректной
    image_id = link.split("/")[5]
    image_url = f"https://drive.google.com/uc?export=view&id={image_id}"
    # Сохраняем ссылку на изображение в стейт вместе с именем модели
    dataForUpdate = {f"{model_name}": image_url}
    await appendDataToStateArray(state, "saved_images_urls", dataForUpdate)

    # Получаем данные родительской папки
    folder = getFolderDataByID(model_data["picture_folder_id"])
    parent_folder_id = folder['parents'][0]
    parent_folder = getFolderDataByID(parent_folder_id)

    logger.info(f"Данные папки по id {model_data['picture_folder_id']}: {folder}")

    # Удаляем текущее сообщение
    await bot.delete_message(user_id, call.message.message_id)

    # Отправляем сообщение о сохранении изображения
    await call.message.answer_photo(
        image_url,
        text.SAVE_IMAGES_SUCCESS_TEXT.format(link, model_name, parent_folder['webViewLink'], model_name_index))

    # Удаляем отправленные изображения из чата
    try:    
        mediagroup_messages_ids = stateData[f"mediagroup_messages_ids_{model_name}"]
        chat_id = call.message.chat.id
        for message_id in mediagroup_messages_ids:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logger.error(f"Произошла ошибка при удалении изображений из чата: {e}")

    # Добавляем в стейт то, сколько сохранённых изображений
    stateData = await state.get_data()
    stateData["saved_images_count"] += 1
    await state.update_data(saved_images_count=stateData["saved_images_count"])

    # Если это была последняя модель в сеансе, то отправляем сообщение о третьем этапе
    if stateData["finally_sent_generated_images_count"] == stateData["saved_images_count"]:
        await call.message.answer(text.SAVING_IMAGE_SUCCESS_TEXT, 
        reply_markup=video_generation_keyboards.generateVideoKeyboard())


# Обработка ввода названия модели для генерации
async def write_model_name_for_generation(message: types.Message, state: FSMContext):
    model_name = message.text
    await state.update_data(model_name_for_generation=model_name)

    # Если такой модели не существует, то просим ввести другое название
    if not await getDataByModelName(model_name):
        await message.answer(text.MODEL_NOT_FOUND_TEXT)
        return

    await message.answer(text.GET_MODEL_NAME_SUCCESS_TEXT)
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

    router.callback_query.register(save_images, lambda call: call.data.startswith("save_images"))

    router.callback_query.register(save_image, lambda call: call.data.startswith("save_image"))

    router.message.register(write_model_name_for_generation, StateFilter(StartGenerationState.write_model_name_for_generation))