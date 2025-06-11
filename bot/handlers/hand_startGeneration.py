import asyncio
import traceback
from datetime import datetime

from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from assets.mocks.links import MOCK_LINK_FOR_SAVE_IMAGE, MOCK_FACEFUSION_PATH
from config import MOCK_MODE, TEMP_FOLDER_PATH, UPSCALE_MODE, FACEFUSION_MODE
from InstanceBot import bot, router
from keyboards import (
    randomizer_keyboards,
    start_generation_keyboards,
    video_generation_keyboards,
)
from logger import logger
from PIL import Image
from states.StartGenerationState import StartGenerationState
from utils import text
from utils.facefusion import facefusion_swap
from utils.generateImages import (
    base64ToImage,
    generateImageBlock,
    imageToBase64,
    upscaleImage,
)
from utils.generateImages.dataArray import (
    getAllDataArrays,
    getDataArrayBySettingNumber,
    getDataByModelName,
    getModelNameIndex,
    getNextModel,
)
from utils.googleDrive.files import saveFile
from utils.googleDrive.folders import getFolderDataByID
from utils.handlers import (
    appendDataToStateArray,
    editMessageOrAnswer,
    deleteMessageFromState
)
from utils.handlers.startGeneration import (
    generateImagesInHandler,
    regenerateImage,
)
from utils.generateImages.dataArray import getSettingNumberByModelName
from utils.googleDrive.files import convertDriveLink

import os


# Обработка выбора количества генераций
async def choose_generations_type(
    call: types.CallbackQuery,
    state: FSMContext,
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
        reply_markup=start_generation_keyboards.selectSettingKeyboard(
            is_test_generation=generations_type == "test",
        ),
    )


# Обработка выбора настройки
async def choose_setting(call: types.CallbackQuery, state: FSMContext):
    # Очищаем стейт
    initial_state = {
        'stop_generation': False,
        'generation_step': 1,
        'prompts_for_regenerate_images': [],
        'regenerate_images': [],
        'model_indexes_for_generation': [],
        'saved_images_urls': [],
        'faceswap_generate_models': [],
        'imageGeneration_mediagroup_messages_ids': [],
        'videoGeneration_messages_ids': []
    }
    
    await state.update_data(**initial_state)

    # Если выбрана конкретная модель, то просим ввести название модели
    if call.data == "select_setting|specific_model":
        await editMessageOrAnswer(
            call,
            text.WRITE_MODELS_NAME_TEXT
        )
        await state.update_data(specific_model=True)
        # Очищаем стейт
        await state.set_state(StartGenerationState.write_model_name_for_generation)
        return 

    # Если выбрана другая настройка, то продолжаем генерацию
    setting_number = call.data.split("|")[1]
    await state.update_data(setting_number=setting_number)
    stateData = await state.get_data()
    generations_type = stateData.get("generations_type", "test")
    prompt_exist = stateData.get("prompt_exist", False)
    await state.update_data(specific_model=False)

    # Если выбрана настройка для теста, то продолжаем генерацию в тестовом режиме
    if generations_type == "test":
        if prompt_exist:
            prompt = stateData.get("prompt_for_images", "")
            user_id = call.from_user.id
            is_test_generation = generations_type == "test"
            setting_number = setting_number

            # Удаляем сообщение с выбором настройки
            await bot.delete_message(user_id, call.message.message_id)

            await generateImagesInHandler(
                prompt,
                call.message,
                state,
                user_id,
                is_test_generation,
                setting_number,
            )

            await state.update_data(prompt_exist=False)
        else:
            await editMessageOrAnswer(
                call,
                text.GET_SETTINGS_SUCCESS_TEXT,
            )
            await state.set_state(StartGenerationState.write_prompt_for_images)

    # Если выбрана настройка для работы, то продолжаем генерацию в рабочем режиме
    elif generations_type == "work":
        await editMessageOrAnswer(
            call,
            text.CHOOSE_WRITE_PROMPT_TYPE_SUCCESS_TEXT,
            reply_markup=start_generation_keyboards.writePromptTypeKeyboard(),
        )


# Обработка выбора режима написания промпта
async def choose_writePrompt_type(
    call: types.CallbackQuery,
    state: FSMContext,
):
    # Получаем данные
    writePrompt_type = call.data.split("|")[1]
    await state.update_data(writePrompt_type=writePrompt_type)

    if writePrompt_type == "one":
        await editMessageOrAnswer(
            call,
            text.GET_ONE_PROMPT_GENERATION_SUCCESS_TEXT,
            reply_markup=start_generation_keyboards.onePromptGenerationChooseTypeKeyboard(),
        )

    else:
        # Получаем данные
        stateData = await state.get_data()
        setting_number = stateData.get("setting_number", 1)

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
            await state.update_data(
                current_setting_number_for_unique_prompt=int(setting_number),
            )

        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

        await editMessageOrAnswer(
            call,
            text.WRITE_PROMPT_FOR_MODEL_START_TEXT.format(
                model_name,
                model_name_index,
            ),
        )
        await state.update_data(current_model_for_unique_prompt=model_name)
        await state.set_state(StartGenerationState.write_prompt_for_model)


# Обработка выбора режима при генерации с одним промптом
async def chooseOnePromptGenerationType(
    call: types.CallbackQuery,
    state: FSMContext,
):
    one_prompt_generation_type = call.data.split("|")[1]

    if one_prompt_generation_type == "static":
        await editMessageOrAnswer(
            call,
            text.GET_STATIC_PROMPT_TYPE_SUCCESS_TEXT,
        )
        await state.set_state(StartGenerationState.write_prompt_for_images)

    elif one_prompt_generation_type == "random":
        # Очищаем все данные, которые используются в рандомайзере
        await state.update_data(variable_names_for_randomizer=[])
        await state.update_data(variable_name_values=[])
        await editMessageOrAnswer(
            call,
            text.GET_RANDOM_PROMPT_TYPE_SUCCESS_TEXT,
            reply_markup=randomizer_keyboards.randomizerKeyboard([]),
        )


# Обработка ввода промпта
async def write_prompt(message: types.Message, state: FSMContext):
    # Получаем данные
    prompt = message.text
    user_id = message.from_user.id
    stateData = await state.get_data()
    is_test_generation = stateData.get("generations_type", "test") == "test"
    await state.update_data(prompt_for_images=prompt)

    await state.set_state(None)

    # Если в стейте есть номер настройки, то используем его, иначе получаем номер настройки по названию модели
    if "setting_number" in stateData:
        setting_number = stateData.get("setting_number", 1)

        # Генерируем изображения
        await generateImagesInHandler(prompt, message, state, user_id, is_test_generation, setting_number)
    else:
        model_indexes = stateData.get("model_indexes_for_generation", [])
        logger.info(f"Список моделей для генерации: {model_indexes}")

        # Генерируем изображения
        await generateImagesInHandler(prompt, message, state, user_id, is_test_generation, "individual")


# Обработка ввода промпта для конкретной модели
async def write_prompt_for_model(message: types.Message, state: FSMContext):
    # Получаем данные
    stateData = await state.get_data()
    prompt = message.text
    model_name = stateData.get("current_model_for_unique_prompt", "")
    setting_number = stateData.get("setting_number", 1)
    user_id = message.from_user.id

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение о начале генерации
    message_for_edit = await message.answer(
        text.GENERATE_IMAGE_PROGRESS_TEXT.format(model_name, model_name_index),
    )

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    # Прибавляем к каждому элементу массива корневой промпт
    json = data["json"].copy()
    json["input"]["prompt"] += " " + prompt

    # Генерируем изображения
    await generateImageBlock(
        json,
        model_name,
        message_for_edit,
        state,
        user_id,
        setting_number,
        False,
        False
    )

    # Получаем следующую модель
    next_model = await getNextModel(model_name, setting_number, state)

    logger.info(f"Следующая модель: {next_model}")

    # Получаем индекс следующей модели
    next_model_index = getModelNameIndex(next_model)

    await state.set_state(None)
    # Просим пользователя отправить промпт для следующей модели
    await message.answer(
        text.WRITE_PROMPT_FOR_MODEL_TEXT.format(next_model, next_model_index),
        reply_markup=start_generation_keyboards.confirmWriteUniquePromptForNextModelKeyboard(),
    )
    await state.update_data(current_model_for_unique_prompt=next_model)


# Обработка нажатия кнопки "✅ Написать промпт" для подтверждения написания уникального промпта для следующей модели
async def confirm_write_unique_prompt_for_next_model(
    call: types.CallbackQuery,
    state: FSMContext,
):
    # Получаем данные
    stateData = await state.get_data()
    next_model = stateData.get("current_model_for_unique_prompt", "")

    # Получаем индекс следующей модели
    next_model_index = getModelNameIndex(next_model)

    # Отправляем сообщение для ввода промпта
    await editMessageOrAnswer(
        call,
        text.WRITE_UNIQUE_PROMPT_FOR_MODEL_TEXT.format(
            next_model,
            next_model_index,
        ),
    )
    await state.set_state(StartGenerationState.write_prompt_for_model)


# Обработка выбора изображения
async def select_image(call: types.CallbackQuery, state: FSMContext):
    # Отправляем сообщение о выборе изображения
    await editMessageOrAnswer(
        call,
        text.SELECT_IMAGE_PROGRESS_TEXT,
    )

    # Получаем id пользователя и данные из стейта
    user_id = call.from_user.id
    stateData = await state.get_data()

    # Получаем индекс работы и индекс изображения
    model_name = call.data.split("|")[1]
    setting_number = call.data.split("|")[2]
    image_index = call.data.split("|")[3]

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    try:

        # Если индекс изображения равен "regenerate", то перегенерируем изображение
        if image_index == "regenerate":
            return await regenerateImage(model_name, call, state, setting_number)
        
        # Если индекс изображения равен "regenerate_with_new_prompt", то перегенерируем изображение с новым промптом
        elif image_index == "regenerate_with_new_prompt":
            # Устанавливаем стейт для ввода нового промпта
            await state.update_data(model_name_for_regenerate_image=model_name)
            await state.update_data(setting_number_for_regenerate_image=setting_number)

            await state.set_state(StartGenerationState.write_new_prompt_for_regenerate_image)

            # Просим ввести новый промпт
            await editMessageOrAnswer(
                call,text.WRITE_NEW_PROMPT_TEXT)
            return
        
        # Если данные не найдены, ищем во всех доступных массивах
        if data is None:
            all_data_arrays = getAllDataArrays()
            for arr in all_data_arrays:
                data = next((d for d in arr if d["model_name"] == model_name), None)
                if data is not None:
                    break

        # Сохраняем название модели и id папки для видео
        await state.update_data(model_name=model_name)

        if not MOCK_MODE:
            # Меняем текст на сообщении о начале upscale
            if UPSCALE_MODE:
                await editMessageOrAnswer(
                    call,text.UPSCALE_IMAGE_PROGRESS_TEXT.format(image_index, model_name, model_name_index))

                # Получаем само изображение по пути
                image_path = (
                    f"{TEMP_FOLDER_PATH}/{model_name}_{user_id}/{image_index}.jpg"
                )
                image = Image.open(image_path)
                image_base64 = imageToBase64(image)

                # Получаем базовую модель
                base_model = data["json"]["input"]["base_model_name"]

                # Получаем номер настройки
                setting_number = getSettingNumberByModelName(model_name)

                # Делаем upscale изображения
                images_output_base64 = await upscaleImage(image_base64, base_model, setting_number, state)

                # Сохраняем изображения по этому же пути
                await base64ToImage(
                    images_output_base64,
                    model_name,
                    int(image_index) - 1,
                    user_id,
                    False,
                )

            if FACEFUSION_MODE:
                # Меняем текст на сообщении об очереди на замену лица
                await editMessageOrAnswer(
                    call,
                    text.FACE_SWAP_WAIT_TEXT.format(model_name, model_name_index),
                )

                # Заменяем лицо на исходном изображении, которое сгенерировалось, на лицо с изображения модели
                faceswap_target_path = (
                    f"images/temp/{model_name}_{user_id}/{image_index}.jpg"
                )
                faceswap_source_path = f"images/faceswap/{model_name}.jpg"
                logger.info(
                    f"Путь к исходному изображению для замены лица: {faceswap_target_path}",
                )
                logger.info(
                    f"Путь к целевому изображению для замены лица: {faceswap_source_path}",
                )

                # Добавляем в стейт путь к изображению для faceswap
                await appendDataToStateArray(
                    state,
                    "faceswap_generate_models",
                    model_name,
                )

                # Запускаем цикл, что пока очередь генераций не освободится, то ответ не будет выдан и генерацию не начинаем
                start_time = datetime.now()
                last_models_state = []

                while True:
                    stateData = await state.get_data()
                    faceswap_generate_models = stateData.get("faceswap_generate_models", [])

                    # Проверяем, изменился ли список моделей
                    if faceswap_generate_models != last_models_state:
                        start_time = datetime.now()
                        last_models_state = faceswap_generate_models.copy()

                    # Проверяем таймаут
                    current_time = datetime.now()
                    elapsed_time = (current_time - start_time).total_seconds()
                    if elapsed_time > 900:  # 15 минут = 900 секунд
                        logger.error(
                            f"Таймаут ожидания обновления списка faceswap_generate_models для модели {model_name}"
                        )
                        await editMessageOrAnswer(
                            call,
                            text.FACE_SWAP_TIMEOUT_ERROR_TEXT.format(
                                model_name,
                                model_name_index,
                            ),
                        )
                        return

                    logger.info(
                        f"Список генераций для замены лица: {faceswap_generate_models}",
                    )

                    # Если список пуст, то завершаем цикл
                    if not len(faceswap_generate_models):
                        break

                    # Если в списке генераций настала очередь этой модели, то запускаем генерацию
                    if model_name == faceswap_generate_models[0]:
                        await editMessageOrAnswer(
                            call,
                            text.FACE_SWAP_PROGRESS_TEXT.format(
                                image_index,
                                model_name,
                                model_name_index,
                            ),
                        )

                        try:
                            result_path = await facefusion_swap(
                                faceswap_source_path,
                                faceswap_target_path,
                            )
                        except Exception as e:
                            result_path = None
                            logger.error(
                                f"Произошла ошибка при замене лица у модели {model_name} с индексом {model_name_index}: {e}",
                            )
                            await editMessageOrAnswer(
                                call,
                                text.FACE_SWAP_ERROR_TEXT.format(
                                    model_name,
                                    model_name_index,
                                    e
                                ),
                            )
                            raise e

                        break

                    await asyncio.sleep(10)

                # После генерации удаляем модель из стейта
                if model_name in faceswap_generate_models:
                    stateData = await state.get_data()
                    faceswap_generate_models = stateData.get("faceswap_generate_models", [])
                    faceswap_generate_models.remove(model_name)
                    await state.update_data(
                        faceswap_models=faceswap_generate_models,
                    )
            else:
                result_path = MOCK_FACEFUSION_PATH

        else:
            result_path = MOCK_FACEFUSION_PATH

        # Если результат замены лица не найден, то завершаем генерацию и уменьшаем кол-во ожидаемых изображений
        if not result_path:
            return

        logger.info(f"Результат замены лица: {result_path}")

        # Меняем текст на сообщении
        saving_progress_message = await editMessageOrAnswer(
            call,
            text.SAVE_IMAGE_PROGRESS_TEXT.format(model_name, model_name_index),
        )

        # Получаем данные модели
        model_data = await getDataByModelName(model_name)

        # Сохраняем изображение
        now = datetime.now().strftime("%Y-%m-%d")
        if not MOCK_MODE:
            link = await saveFile(
                result_path,
                user_id,
                model_name,
                model_data["picture_folder_id"],
                now,
            )
        else:
            link = MOCK_LINK_FOR_SAVE_IMAGE

        # Конвертируем ссылку в прямую ссылку для скачивания
        direct_url = convertDriveLink(link)

        dataForUpdate = {f"{model_name}": direct_url}
        await appendDataToStateArray(state, "saved_images_urls", dataForUpdate)

        if not link:
            traceback.print_exc()
            await editMessageOrAnswer(
                call,
                text.SAVE_FILE_ERROR_TEXT.format(model_name, model_name_index),
            )
            return

        # Получаем данные родительской папки
        folder = getFolderDataByID(model_data["picture_folder_id"])
        parent_folder_id = folder["parents"][0]
        parent_folder = getFolderDataByID(parent_folder_id)

        logger.info(
            f"Данные папки по id {model_data['picture_folder_id']}: {folder}",
        )

        # Отправляем сообщение о сохранении изображения
        logger.info(f"Отправляем сообщение о сохранении изображения: {direct_url}")
        await call.message.answer_photo(
            direct_url,
            text.SAVE_IMAGES_SUCCESS_TEXT.format(
                link,
                model_name,
                parent_folder["webViewLink"],
                model_name_index,
            ),
            reply_markup=video_generation_keyboards.generateVideoKeyboard(model_name)
        )

        # Удаляем сообщение о сохранении изображения
        await saving_progress_message.delete()

        # Удаляем изображение с замененным лицом
        if not MOCK_MODE:
            os.remove(result_path)

        # Удаляем медиагруппу
        await deleteMessageFromState(state, "imageGeneration_mediagroup_messages_ids", model_name, call.message.chat.id)

    except Exception as e:
        traceback.print_exc()
        await editMessageOrAnswer(
            call,
            text.GENERATE_IMAGE_ERROR_TEXT.format(model_name, e),
        )
        raise e


# Обработка ввода названия модели для генерации
async def write_model_name_for_generation(message: types.Message, state: FSMContext):
    # Если в сообщении есть запятые, то записываем массив моделей в стейт
    model_indexes = message.text.split(",")
    
    # Если запятых нет, то записываем одну модель в стейт
    if len(model_indexes) == 1:
        model_indexes = [message.text]
    
    # Удаляем пробелы из названий моделей
    model_indexes = [model_index.strip() for model_index in model_indexes]

    # Проверяем, что это число
    for model_index in model_indexes:
        if not model_index.isdigit():
            await message.answer(text.MODEL_NOT_FOUND_TEXT.format(model_index))
            return
    
    # Проверяем, существует ли такие модели
    for model_index in model_indexes:
        # Если индекс больше 100 или меньше 1, то просим ввести другой индекс
        if int(model_index) > 100 or int(model_index) < 1:
            await message.answer(text.MODEL_NOT_FOUND_TEXT.format(model_index))
            return
        
    await state.update_data(model_indexes_for_generation=model_indexes)

    await state.set_state(None)
    await message.answer(text.GET_MODEL_INDEX_SUCCESS_TEXT if len(model_indexes) == 1 else text.GET_MODEL_INDEXES_SUCCESS_TEXT)
    await state.set_state(StartGenerationState.write_prompt_for_images)


# Обработка ввода нового промпта для перегенерации изображения
async def write_new_prompt_for_regenerate_image(message: types.Message, state: FSMContext):
    # Получаем данные
    stateData = await state.get_data()
    is_test_generation = stateData.get("generations_type", "test") == "test"
    model_name = stateData.get("model_name_for_regenerate_image", "")
    setting_number = stateData.get("setting_number_for_regenerate_image", 1)
    prompt = message.text
    user_id = message.from_user.id

    # Записываем новый промпт в стейт для этой модели
    dataForUpdate = {f"{model_name}": prompt}
    await appendDataToStateArray(state, "prompts_for_regenerate_images", dataForUpdate)

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение о перегенерации изображения
    await message.answer(text.REGENERATE_IMAGE_WITH_NEW_PROMPT_TEXT.format(model_name, model_name_index, prompt))

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    # Прибавляем к каждому элементу массива корневой промпт
    json = data["json"].copy()
    json["input"]["prompt"] += " " + prompt 
    
    await state.set_state(None)
    return await generateImageBlock(json, model_name, message, state, user_id, setting_number, is_test_generation, False)


# Добавление обработчиков
def hand_add():
    router.callback_query.register(
        choose_generations_type,
        lambda call: call.data.startswith("generations_type"),
    )

    router.callback_query.register(
        choose_setting,
        lambda call: call.data.startswith("select_setting"),
    )

    router.callback_query.register(
        choose_writePrompt_type,
        lambda call: call.data.startswith("write_prompt_type"),
    )

    router.callback_query.register(
        chooseOnePromptGenerationType,
        lambda call: call.data.startswith("one_prompt_generation_type"),
    )

    router.message.register(
        write_prompt,
        StateFilter(StartGenerationState.write_prompt_for_images),
    )

    router.message.register(
        write_prompt_for_model,
        StateFilter(StartGenerationState.write_prompt_for_model),
    )

    router.callback_query.register(
        confirm_write_unique_prompt_for_next_model,
        lambda call: call.data.startswith(
            "confirm_write_unique_prompt_for_next_model",
        ),
    )

    router.callback_query.register(
        select_image,
        lambda call: call.data.startswith("select_image"),
    )

    router.message.register(write_model_name_for_generation, StateFilter(StartGenerationState.write_model_name_for_generation))

    router.message.register(write_new_prompt_for_regenerate_image, StateFilter(StartGenerationState.write_new_prompt_for_regenerate_image))