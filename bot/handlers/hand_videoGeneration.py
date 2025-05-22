from utils import retryOperation
from utils.videos.generateVideo import generateVideo
from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from utils.videoExamples.getVideoExampleDataByIndex import getVideoExampleDataByIndex
from utils.saveImages.getFolderDataByID import getFolderDataByID
from utils.files.saveFile import saveFile
from keyboards import video_generation_keyboards
from utils import text
from states import StartGenerationState
from logger import logger
from InstanceBot import bot
import traceback
from utils.videoExamples.getVideoExamplesData import getVideoExamplesData
from InstanceBot import router
import os
from datetime import datetime
from utils.generateImages.dataArray.getModelNameIndex import getModelNameIndex
from utils.handlers.editMessageOrAnswer import editMessageOrAnswer


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
    select_video_example_message = await editMessageOrAnswer(
        call,text.SELECT_VIDEO_EXAMPLE_TEXT.format(model_name, model_name_index))

    await state.update_data(select_video_example_message_id=select_video_example_message.message_id)

    # Получаем все видео-шаблоны с их промптами
    templates_examples = await getVideoExamplesData()

    # Выгружаем видео-примеры вместе с их промптами
    video_examples_messages_ids = []
    for index, value in templates_examples.items():
        video_example_message = await editMessageOrAnswer_video(
            video=value["file_id"],
            caption=text.VIDEO_EXAMPLE_TEXT.format(model_name, model_name_index, value["prompt"]),
            reply_markup=video_generation_keyboards.videoExampleKeyboard(index, model_name)
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
        await editMessageOrAnswer(
        call,text.WRITE_PROMPT_FOR_VIDEO_TEXT.format(model_name, model_name_index))
        await state.set_state(StartGenerationState.write_prompt_for_video)
        return
    
    # Отправляем сообщение под генерацию видео
    message_for_delete = await editMessageOrAnswer(
        call,text.GENERATE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index))

    # Генерируем видео
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
    await state.update_data(video_path=video_path)

    # Удаляем сообщение про генерацию видео
    await bot.delete_message(user_id, message_for_delete.message_id)

    # Отправляем видео
    video = types.FSInputFile(video_path)
    if button_type == "test":
        await editMessageOrAnswer_video(video=video, caption=text.GENERATE_TEST_VIDEO_SUCCESS_TEXT.format(model_name), 
        reply_markup=video_generation_keyboards.videoExampleKeyboard(index, model_name, False))

    elif button_type == "work":
        await editMessageOrAnswer_video(video=video, caption=text.GENERATE_VIDEO_SUCCESS_TEXT.format(model_name, model_name_index), 
        reply_markup=video_generation_keyboards.videoCorrectnessKeyboard(model_name))


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
    reply_markup=video_generation_keyboards.videoExampleKeyboard(index, data["model_name"], with_write_prompt=False))


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
        message_for_edit = await editMessageOrAnswer(
        call,text.SAVE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index))

        # Сохраняем видео
        link = await saveFile(video_path, user_id, model_name, video_folder_id, now, False)

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

        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

        # Отправляем сообщение о сохранении видео
        await message_for_edit.answer(text.SAVE_VIDEO_SUCCESS_TEXT
        .format(link, model_name, parent_folder['webViewLink'], model_name_index))

        # Удаляем видео из папки temp/videos
        os.remove(video_path)


# Добавление обработчиков
def hand_add():
    router.callback_query.register(start_generate_video, lambda call: call.data.startswith("start_generate_video"))

    router.callback_query.register(handle_video_example_buttons, lambda call: call.data.startswith("generate_video"))

    router.message.register(write_prompt_for_video, StateFilter(StartGenerationState.write_prompt_for_video))

    router.callback_query.register(handle_video_correctness_buttons, 
    lambda call: call.data.startswith("video_correctness"))
