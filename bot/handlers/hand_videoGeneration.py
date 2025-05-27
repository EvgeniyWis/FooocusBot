from utils.handlers import increaseCountInState
from utils.handlers import appendDataToStateArray
from assets.mocks.links import MOCK_LINK_FOR_SAVE_VIDEO
from utils.handlers.videoGeneration import sendNextModelMessage
from utils import retryOperation, text
from utils.videos import generateVideo
from utils.videoExamples import getVideoExampleDataByIndex, getVideoExamplesData
from utils.generateImages.dataArray import getModelNameIndex
from utils.handlers import editMessageOrAnswer
from utils.googleDrive.files import saveFile
from utils.googleDrive.folders import getFolderDataByID
from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards import video_generation_keyboards
from states import StartGenerationState
from logger import logger
from InstanceBot import bot
import traceback
from InstanceBot import router
import os
from datetime import datetime
from config import MOCK_MODE


# Обработка нажатия кнопки "📹 Сгенерировать видео"
async def start_generate_video(call: types.CallbackQuery, state: FSMContext):
    temp = call.data.split("|")
    if len(temp) == 2:
        model_name = temp[1]
    else:
        model_name = None

    # Отправляем сообщение для первой модели
    await sendNextModelMessage(state, call, model_name)


# Обработка нажатия кнопок режима генерации видео
async def handle_video_generation_mode_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем индекс модели
    model_name = call.data.split("|")[1]
    model_name_index = getModelNameIndex(model_name)

    # Получаем выбранный режим генерации видео
    mode = call.data.split("|")[2]

    # Если выбран режим "Написать свой промпт", то отправляем сообщение для ввода кастомного промпта
    if mode == "write_prompt":
        await state.update_data(model_name_for_video_generation=model_name)
        await editMessageOrAnswer(
        call,text.WRITE_PROMPT_FOR_VIDEO_TEXT.format(model_name, model_name_index))
        await state.set_state(StartGenerationState.write_prompt_for_video)
        return

    # TODO: режим генерации видео с видео-примерами временно отключен
    # Если выбран режим "Использовать заготовленные примеры", то отправляем сообщение с видео-примерами
    # elif mode == "use_examples":
    #     # Получаем все видео-шаблоны с их промптами
    #     templates_examples = await getVideoExamplesData()

    #     # Выгружаем видео-примеры вместе с их промптами
    #     video_examples_messages_ids = []
    #     for index, value in templates_examples.items():
    #         video_example_message = await call.message.answer_video(
    #             video=value["file_id"],
    #             caption=text.VIDEO_EXAMPLE_TEXT.format(model_name, model_name_index, value["prompt"]),
    #             reply_markup=video_generation_keyboards.generatedVideoKeyboard(f"generate_video|{index}|{model_name}")
    #         )
    #         video_examples_messages_ids.append(video_example_message.message_id)
    #         await state.update_data(video_examples_messages_ids=video_examples_messages_ids)


# Обработка нажатия кнопок под видео-примером
async def handle_video_example_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем индекс видео-примера и тип кнопки
    temp = call.data.split("|")

    if len(temp) == 4:
        # TODO: режим генерации видео с видео-примерами временно отключен
        # index = int(temp[1])
        model_name = temp[2]
        button_type = temp[3]
        # await state.update_data(video_example_index=index)
    else:
        model_name = temp[1]
        button_type = temp[2]

    user_id = call.from_user.id
    await state.update_data(type_for_video_generation=button_type)

    # Получаем название модели и url изображения
    data = await state.get_data()
    image_url = data["image_url"]

    # Удаляем сообщение с выбором видео-примера
    # TODO: режим генерации видео с видео-примерами временно отключен
    # try:
    #     await bot.delete_message(user_id, int(data["select_video_example_message_id"]))
    # except Exception as e:
    #     logger.error(f"Произошла ошибка при удалении сообщения с id {data['select_video_example_message_id']}: {e}")

    # if len(temp) == 4:
    #     # Получаем данные видео-примера по его индексу
    #     video_example_data = await getVideoExampleDataByIndex(index)

    # Получаем кастомный промпт, если он есть, а если нет, то берем промпт из видео-примера 
    if "prompt_for_video" in data:
        custom_prompt = data["prompt_for_video"]
    else:
        custom_prompt = None

    # TODO: режим генерации видео с видео-примерами временно отключен, поэтому кастомный промпт используется
    video_example_prompt = custom_prompt
    
    # TODO: режим генерации видео с видео-примерами временно отключен
    # if custom_prompt:
    #     video_example_prompt = custom_prompt
    # else:
    #     video_example_prompt = video_example_data["prompt"]

    # # Удаляем сообщения с видео-примерами
    # if "video_examples_messages_ids" in data:
    #     video_examples_messages_ids = data["video_examples_messages_ids"]

    #     for message_id in video_examples_messages_ids:
    #         try:
    #             await bot.delete_message(user_id, int(message_id))
    #         except Exception as e:
    #             logger.error(f"Произошла ошибка при удалении сообщения с id {message_id}: {e}")
                
    # Удаляем текущее сообщение
    try:
        await bot.delete_message(user_id, call.message.message_id)
    except Exception as e:
        logger.error(f"Произошла ошибка при удалении сообщения с id {call.message.message_id}: {e}")

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)
    
    # Отправляем сообщение про генерацию видео
    message_for_delete = await editMessageOrAnswer(
        call,text.GENERATE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index))
    
    # Удаляем из очереди текущую модель
    stateData = await state.get_data()
    stateData["saved_images_urls"].pop(0)
    await state.update_data(saved_images_urls=stateData["saved_images_urls"])
    
    # Отправляем следующую модель
    await sendNextModelMessage(state, call)

    # Добавляем повторно дату в стейт
    dataForUpdate = {f"{model_name}": image_url}
    stateData["saved_images_urls"].append(dataForUpdate)
    await state.update_data(saved_images_urls=stateData["saved_images_urls"])

    # Увеличиваем счётчик того, сколько уже отправилось моделей
    await increaseCountInState(state, "sent_videos_count")

    # Проверяем, что модель последняя в генерации
    stateData = await state.get_data()
    if stateData["sent_videos_count"] == len(stateData["saved_images_urls"]):
        await call.message.answer(text.SAVING_VIDEOS_SUCCESS_TEXT, 
        reply_markup=video_generation_keyboards.saveVideoKeyboard())

    # Генерируем видео
    if MOCK_MODE:
        video_path = "FocuuusBot/bot/assets/mocks/mock_video.mp4"
    else:
        try:
            video_path = await retryOperation(generateVideo, 10, 1.5, video_example_prompt, image_url)
        except Exception as e:
                
            # Удаляем сообщение про генерацию видео
            await bot.delete_message(user_id, message_for_delete.message_id)

            # Отправляем сообщение об ошибке
            traceback.print_exc()
            await editMessageOrAnswer(
            call,text.GENERATE_VIDEO_ERROR_TEXT.format(model_name, e))
            logger.error(f"Произошла ошибка при генерации видео для модели {model_name}: {e}")
            return
    
    # Сохраняем видео в стейт
    await appendDataToStateArray(state, "generated_video_paths", video_path)


# Хедлер для обработки ввода кастомного промпта для видео
async def write_prompt_for_video(message: types.Message, state: FSMContext):
    # Получаем данные
    prompt = message.text
    await state.update_data(prompt_for_video=prompt)
    data = await state.get_data()
    image_url = data["image_url"]

    # Отправляем видео
    model_name = data["model_name_for_video_generation"]

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)
    
    await message.answer_photo(
    photo=image_url,
    caption=text.WRITE_PROMPT_FOR_VIDEO_SUCCESS_TEXT.format(model_name, model_name_index, prompt),
    reply_markup=video_generation_keyboards.generatedVideoKeyboard(f"generate_video|{model_name}"))


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

        # Удаляем из очереди текущую модель
        stateData = await state.get_data()
        stateData["saved_images_urls"].pop(0)
        await state.update_data(saved_images_urls=stateData["saved_images_urls"])

        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

        # Отправляем сообщение о начале сохранения видео
        message_for_edit = await editMessageOrAnswer(
        call,text.SAVE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index))

        # Сохраняем видео
        if not MOCK_MODE:
            link = await saveFile(video_path, user_id, model_name, video_folder_id, now, False)
        else:
            link = MOCK_LINK_FOR_SAVE_VIDEO

        if not link:
            await editMessageOrAnswer(
        call,text.SAVE_FILE_ERROR_TEXT)
            return
        
        # Получаем данные родительской папки
        folder = getFolderDataByID(video_folder_id)
        parent_folder_id = folder['parents'][0]
        parent_folder = getFolderDataByID(parent_folder_id)

        logger.info(f"Данные папки по id {video_folder_id}: {folder}")

        # Удаляем сообщение про генерацию видео
        await bot.delete_message(user_id, message_for_edit.message_id)

        # Отправляем сообщение о сохранении видео
        await message_for_edit.answer(text.SAVE_VIDEO_SUCCESS_TEXT
        .format(link, model_name, parent_folder['webViewLink'], model_name_index))

        # Удаляем видео из папки temp/videos
        if not MOCK_MODE:
            os.remove(video_path)

        # Добавляем в стейт, сколько видео сгенерилось
        await increaseCountInState(state, "saved_videos_count")

        # Если это было последнее видео, то отправляем сообщение о заканчивании генерации
        if len(stateData["saved_images_urls"]) == stateData["saved_videos_count"] + 1 and not stateData["specific_model"]:
            await call.message.answer(text.SAVING_VIDEOS_SUCCESS_TEXT)


# Хендлер для сохранения видео
async def start_save_video(call: types.CallbackQuery, state: FSMContext):
    # Получаем первую модель в очереди
    stateData = await state.get_data()
    model_name = list(stateData["generated_video_paths"][0].keys())[0]
    video_path = stateData["generated_video_paths"][0][model_name]

    # Получаем тип генерации
    type_for_video_generation = stateData["type_for_video_generation"]

    # Отправляем видео
    video = types.FSInputFile(video_path)
    if type_for_video_generation == "test":
        # TODO: режим генерации видео с видео-примерами временно отключен
        # if "video_example_index" in stateData:
        #     prefix = f"generate_video|{stateData['video_example_index']}|{model_name}"
        # else:
        #     prefix = f"generate_video|{model_name}"

        prefix = f"generate_video|{model_name}"

        await call.message.answer_video(video=video, caption=text.GENERATE_TEST_VIDEO_SUCCESS_TEXT.format(model_name), 
        reply_markup=video_generation_keyboards.generatedVideoKeyboard(prefix, False))

    elif type_for_video_generation == "work":
        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

        await call.message.answer_video(video=video, caption=text.GENERATE_VIDEO_SUCCESS_TEXT.format(model_name, model_name_index), 
        reply_markup=video_generation_keyboards.videoCorrectnessKeyboard(model_name))



# Добавление обработчиков
def hand_add():
    router.callback_query.register(start_generate_video, lambda call: call.data == "start_generate_video")

    router.callback_query.register(handle_video_generation_mode_buttons, lambda call: call.data.startswith("generate_video_mode"))

    router.callback_query.register(handle_video_example_buttons, lambda call: call.data.startswith("generate_video"))

    router.message.register(write_prompt_for_video, StateFilter(StartGenerationState.write_prompt_for_video))

    router.callback_query.register(handle_video_correctness_buttons, 
    lambda call: call.data.startswith("video_correctness"))

    router.callback_query.register(start_save_video, lambda call: call.datа == "start_save_video")
