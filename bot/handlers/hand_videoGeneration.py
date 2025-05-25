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
    
    # Если выбран режим "Использовать заготовленные примеры", то отправляем сообщение с видео-примерами
    elif mode == "use_examples":
        # Получаем все видео-шаблоны с их промптами
        templates_examples = await getVideoExamplesData()

        # Выгружаем видео-примеры вместе с их промптами
        video_examples_messages_ids = []
        for index, value in templates_examples.items():
            video_example_message = await call.message.answer_video(
                video=value["file_id"],
                caption=text.VIDEO_EXAMPLE_TEXT.format(model_name, model_name_index, value["prompt"]),
                reply_markup=video_generation_keyboards.videoExampleKeyboard(f"generate_video|{index}|{model_name}")
            )
            video_examples_messages_ids.append(video_example_message.message_id)
            await state.update_data(video_examples_messages_ids=video_examples_messages_ids)


# Обработка нажатия кнопок под видео-примером
async def handle_video_example_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем индекс видео-примера и тип кнопки
    temp = call.data.split("|")

    if len(temp) == 4:
        index = int(temp[1])
        model_name = temp[2]
        button_type = temp[3]
    else:
        model_name = temp[1]
        button_type = temp[2]

    user_id = call.from_user.id

    # Получаем название модели и url изображения
    data = await state.get_data()
    image_url = data["image_url"]

    # Удаляем сообщение с выбором видео-примера
    try:
        await bot.delete_message(user_id, int(data["select_video_example_message_id"]))
    except Exception as e:
        logger.error(f"Произошла ошибка при удалении сообщения с id {data['select_video_example_message_id']}: {e}")

    if len(temp) == 4:
        # Получаем данные видео-примера по его индексу
        video_example_data = await getVideoExampleDataByIndex(index)

    # Получаем кастомный промпт, если он есть, а если нет, то берем промпт из видео-примера 
    if "prompt_for_video" in data:
        custom_prompt = data["prompt_for_video"]
    else:
        custom_prompt = None
    
    if custom_prompt:
        video_example_prompt = custom_prompt
    else:
        video_example_prompt = video_example_data["prompt"]

    # Удаляем сообщения с видео-примерами
    if "video_examples_messages_ids" in data:
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

    # Генерируем видео
    # TODO: убрать заглушку
    # try:
    #     video_path = await retryOperation(generateVideo, 10, 1.5, video_example_prompt, image_url)
    # except Exception as e:
    #     # Удаляем сообщение про генерацию видео
    #     await bot.delete_message(user_id, message_for_delete.message_id)

    #     # Отправляем сообщение об ошибке
    #     traceback.print_exc()
    #     await editMessageOrAnswer(
    #     call,text.GENERATE_VIDEO_ERROR_TEXT.format(model_name, e))
    #     logger.error(f"Произошла ошибка при генерации видео для модели {model_name}: {e}")
    #     return

    video_path = "FocuuusBot/video.mp4"
    
    # Сохраняем видео в стейт
    await state.update_data(video_path=video_path)

    # Удаляем сообщение про генерацию видео
    await bot.delete_message(user_id, message_for_delete.message_id)

    # Отправляем видео
    video = types.FSInputFile(video_path)
    if button_type == "test":
        if len(temp) == 4:
            prefix = f"generate_video|{index}|{model_name}"
        else:
            prefix = f"generate_video|{model_name}"

        await call.message.answer_video(video=video, caption=text.GENERATE_TEST_VIDEO_SUCCESS_TEXT.format(model_name), 
        reply_markup=video_generation_keyboards.videoExampleKeyboard(prefix, False))

    elif button_type == "work":
        await call.message.answer_video(video=video, caption=text.GENERATE_VIDEO_SUCCESS_TEXT.format(model_name, model_name_index), 
        reply_markup=video_generation_keyboards.videoCorrectnessKeyboard(model_name))


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
    reply_markup=video_generation_keyboards.videoExampleKeyboard(f"generate_video|{model_name}"))


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
        # TODO: раскомментировать
        # link = await saveFile(video_path, user_id, model_name, video_folder_id, now, False)
        link = "https://drive.google.com/drive/folders/18V64itY-c07U43aZb09mdzgVU9UGa242"

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
        # TODO: раскомментировать
        # os.remove(video_path)

        # Добавляем в стейт, сколько видео сгенерилось
        stateData = await state.get_data()
        stateData["saved_videos_count"] += 1
        await state.update_data(saved_images_count=stateData["saved_images_count"])

        # Если это было последнее видео, то отправляем сообщение о заканчивании генерации
        if stateData["saved_images_count"] == stateData["saved_videos_count"] + 1 and not stateData["specific_model"]:
            await call.message.answer(text.SAVING_VIDEOS_SUCCESS_TEXT)


# Добавление обработчиков
def hand_add():
    router.callback_query.register(start_generate_video, lambda call: call.data.startswith("start_generate_video"))

    router.callback_query.register(handle_video_generation_mode_buttons, lambda call: call.data.startswith("generate_video_mode"))

    router.callback_query.register(handle_video_example_buttons, lambda call: call.data.startswith("generate_video"))

    router.message.register(write_prompt_for_video, StateFilter(StartGenerationState.write_prompt_for_video))

    router.callback_query.register(handle_video_correctness_buttons, 
    lambda call: call.data.startswith("video_correctness"))
