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
from states.UserState import StartGenerationState
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
    increaseCountInState,
)
from utils.handlers.startGeneration import (
    generateImagesInHandler,
    regenerateImage,
    sendMessageForImageSaving,
    waitForImageBlocksGeneration,
)
from utils.generateImages.dataArray import getSettingNumberByModelName


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
    data = await state.get_data()
    generations_type = data["generations_type"]
    prompt_exist = data["prompt_exist"]
    await state.update_data(specific_model=False)

    # Если выбрана настройка для теста, то продолжаем генерацию в тестовом режиме
    if generations_type == "test":
        if prompt_exist:
            prompt = data["prompt_for_images"]
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
        await state.update_data(total_images_count=0)
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
        setting_number = getSettingNumberByModelName(model_names[0])

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

    # Сохраняем промпт в стейт под конкретную модель
    dataForUniquePrompts = {"model_name": model_name, "prompt": prompt}
    await appendDataToStateArray(state, "unique_prompts_for_models", dataForUniquePrompts)

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение о начале генерации
    message_for_edit = await message.answer(
        text.GENERATE_IMAGE_PROGRESS_TEXT.format(model_name, model_name_index),
    )

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    # Прибавляем к каждому элементу массива корневой промпт
    data["json"]["input"]["prompt"] += " " + prompt

    # Генерируем изображения
    await state.update_data(media_groups_for_generation=None)
    await generateImageBlock(
        data["json"],
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
    data = await state.get_data()
    next_model = data["current_model_for_unique_prompt"]

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
    # Получаем id пользователя и данные из стейта
    user_id = call.from_user.id
    stateData = await state.get_data()

    # Получаем индекс работы и индекс изображения
    model_name = call.data.split("|")[1]
    setting_number = call.data.split("|")[2]
    image_index = call.data.split("|")[3]

    # Если это режим генерации для конкретной модели, то не ждём пока появится следующий блок изображений в очереди
    stateData = await state.get_data()
    next_model_name = False

    if not stateData["specific_model"]:
        # Отправляем следующее изображение (ждём пока появится следующий блок изображений в очереди и отправляем его)
        next_model_name = asyncio.create_task(
            waitForImageBlocksGeneration(call.message, state, user_id),
        )

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
    
        # Добавляем в стейт то, сколько отправленных изображений
        await increaseCountInState(
            state,
            "will_be_sent_generated_images_count",
        )

        # Если данные не найдены, ищем во всех доступных массивах
        if data is None:
            all_data_arrays = getAllDataArrays()
            for arr in all_data_arrays:
                data = next((d for d in arr if d["model_name"] == model_name), None)
                if data is not None:
                    break

        video_folder_id = data["video_folder_id"]

        # Сохраняем название модели и id папки для видео
        await state.update_data(model_name=model_name)
        await state.update_data(video_folder_id=video_folder_id)

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
                images_output_base64 = await upscaleImage(image_base64, base_model, setting_number)

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
                while True:
                    stateData = await state.get_data()
                    faceswap_generate_models = stateData[
                        "faceswap_generate_models"
                    ]

                    logger.info(
                        f"Список генераций для замены лица: {faceswap_generate_models}",
                    )

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
                                ),
                            )
                            break

                        break

                    await asyncio.sleep(10)

                # После генерации удаляем модель из стейта
                stateData = await state.get_data()
                stateData["faceswap_generate_models"].remove(model_name)
                await state.update_data(
                    faceswap_models=stateData["faceswap_generate_models"],
                )
            else:
                result_path = MOCK_FACEFUSION_PATH

        else:
            result_path = MOCK_FACEFUSION_PATH

        # Если результат замены лица не найден, то завершаем генерацию и уменьшаем кол-во ожидаемых изображений
        if not result_path:
            await increaseCountInState(
                state,
                "will_be_sent_generated_images_count",
                -1
            )
            return

        logger.info(f"Результат замены лица: {result_path}")

        if stateData["generation_step"] == 1:
            # Добавляем result_path в стейт
            updateData = {f"{model_name}": result_path}
            await appendDataToStateArray(state, "generated_images", updateData)

            stateData = await state.get_data()
            logger.info(
                f"Список сгенерируемых изображений для сохранения: {stateData['generated_images']}",
            )

            # Меняем текст на сообщении
            await editMessageOrAnswer(
                call,
                text.FACE_SWAP_SUCCESS_TEXT.format(
                    model_name,
                    model_name_index,
                ),
                reply_markup=start_generation_keyboards.saveImagesKeyboard()
                if stateData["specific_model"]
                else None,
            )

            # Добавляем в стейт то, сколько отправленных изображений
            await increaseCountInState(
                state,
                "finally_sent_generated_images_count",
            )

            # Проверяем, что количество отправленных изображений и тех, которые собираются отправиться, равно
            stateData = await state.get_data()
            generation_is_finished = (
                stateData["finally_sent_generated_images_count"]
                >= stateData["will_be_sent_generated_images_count"] and
                stateData["finally_sent_generated_images_count"]
                >= stateData["total_images_count"] 
            )

            if generation_is_finished:
                # И только после этого отправляем сообщение о успешной генерации с возможностью начать этап сохранения изображений
                await call.message.answer(
                    text.GENERATE_IMAGES_SUCCESS_TEXT,
                    reply_markup=start_generation_keyboards.saveImagesKeyboard(),
                )

                # Ставим, что начался 2 этап
                await state.update_data(generation_step=2)

        elif stateData["generation_step"] == 2:
            await call.message.edit_text(
                text.GENERATE_IMAGE_SUCCESS_TEXT,
                reply_markup=start_generation_keyboards.saveImagesKeyboard(),
        )

    except Exception as e:
        traceback.print_exc()
        logger.error(f"Произошла ошибка при генерации изображения: {e}")
        await editMessageOrAnswer(
            call,
            text.GENERATE_IMAGE_ERROR_TEXT.format(model_name, e),
        )

    finally:
        if next_model_name and not stateData["specific_model"]:
            # Удаляем модель из очереди генерации
            stateData = await state.get_data()
            next_model_name = await next_model_name

            if not next_model_name:
                return

            logger.info(
                f"Удаляем модель из очереди генерации: {next_model_name} из списка: {stateData['models_for_generation_queue']}",
            )
            stateData["models_for_generation_queue"].remove(next_model_name)
            await state.update_data(
                models_for_generation_queue=stateData[
                    "models_for_generation_queue"
                ],
            )


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
        call,
        text.SAVE_IMAGE_PROGRESS_TEXT.format(model_name, model_name_index),
    )

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

    if not link:
        traceback.print_exc()
        await editMessageOrAnswer(
            call,
            text.SAVE_FILE_ERROR_TEXT.format(model_name, model_name_index),
        )
        return

    # Делаем ссылку корректной
    image_id = link.split("/")[5]
    image_url = f"https://drive.google.com/uc?export=view&id={image_id}"

    # Получаем данные родительской папки
    folder = getFolderDataByID(model_data["picture_folder_id"])
    parent_folder_id = folder["parents"][0]
    parent_folder = getFolderDataByID(parent_folder_id)

    logger.info(
        f"Данные папки по id {model_data['picture_folder_id']}: {folder}",
    )

    # Удаляем текущее сообщение
    await bot.delete_message(user_id, call.message.message_id)

    # Отправляем сообщение о сохранении изображения
    logger.info(f"Отправляем сообщение о сохранении изображения: {image_url}")
    await call.message.answer_photo(
        image_url,
        text.SAVE_IMAGES_SUCCESS_TEXT.format(
            link,
            model_name,
            parent_folder["webViewLink"],
            model_name_index,
        ),
    )

    # Удаляем отправленные изображения из чата
    # try:
    #     mediagroup_messages_ids = stateData[
    #         f"mediagroup_messages_ids_{model_name}"
    #     ]
    #     chat_id = call.message.chat.id
    #     for message_id in mediagroup_messages_ids:
    #         await bot.delete_message(chat_id=chat_id, message_id=message_id)
    # except Exception as e:
    #     logger.error(f"Произошла ошибка при удалении изображений из чата: {e}")

    # Сохраняем ссылку на изображение в стейт вместе с именем модели
    dataForUpdate = {f"{model_name}": image_url}
    await appendDataToStateArray(state, "saved_images_urls", dataForUpdate)

    # Если это была последняя модель в сеансе, то отправляем сообщение о третьем этапе
    stateData = await state.get_data()
    if stateData["finally_sent_generated_images_count"] == len(
        stateData["saved_images_urls"],
    ):
        await call.message.answer(
            text.SAVING_IMAGES_SUCCESS_TEXT,
            reply_markup=video_generation_keyboards.generateVideoKeyboard(),
        )

        # Делаем стейт images_urls_for_videos
        logger.info(f"Список сохранённых изображений на момент перед генерацией видео: {stateData['saved_images_urls']}")
        images_urls_for_videos = [item for item in stateData["saved_images_urls"]]
        await state.update_data(images_urls_for_videos=images_urls_for_videos)


# Обработка ввода названия модели для генерации
async def write_model_name_for_generation(message: types.Message, state: FSMContext):
    # Если в сообщении есть запятые, то записываем массив моделей в стейт
    model_names = message.text.split(",")
    
    # Если запятых нет, то записываем одну модель в стейт
    if len(model_names) == 1:
        model_names = [message.text]
    else:
        await state.update_data(specific_model=False)
    
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


# Обработка ввода нового промпта для перегенерации изображения
async def write_new_prompt_for_regenerate_image(message: types.Message, state: FSMContext):
    # Получаем данные
    stateData = await state.get_data()
    is_test_generation = stateData["generations_type"] == "test"
    model_name = stateData["model_name_for_regenerate_image"]
    setting_number = stateData["setting_number_for_regenerate_image"]
    prompt = message.text
    user_id = message.from_user.id

    # Записываем новый промпт в стейт для этой модели
    dataForUpdate = {f"{model_name}": prompt}
    if "prompts_for_regenerate_images" not in stateData:
        await state.update_data(prompts_for_regenerate_images=dataForUpdate)
    else:
        stateData["prompts_for_regenerate_images"][model_name] = prompt
        await state.update_data(prompts_for_regenerate_images=stateData["prompts_for_regenerate_images"])

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение о перегенерации изображения
    await message.answer(text.REGENERATE_IMAGE_WITH_NEW_PROMPT_TEXT.format(model_name, model_name_index, prompt))

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    # Прибавляем к каждому элементу массива корневой промпт
    data["json"]['input']['prompt'] += " " + prompt 
    
    # Добавляем модель в массив перегенируемых изображений
    await appendDataToStateArray(state, "regenerate_images", model_name)

    return await generateImageBlock(data["json"], model_name, message, state, user_id, setting_number, is_test_generation, False)


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
    router.callback_query.register(
        save_images,
        lambda call: call.data.startswith("save_images"),
    )

    router.callback_query.register(
        save_image,
        lambda call: call.data.startswith("save_image"),
    )
