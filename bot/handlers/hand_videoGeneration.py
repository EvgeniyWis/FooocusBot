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
import asyncio
from utils.handlers.videoGeneration.saveVideo import saveVideo
from utils.generateImages.dataArray.getDataByModelName import getDataByModelName


# Обработка нажатия кнопки "📹 Сгенерировать видео"
async def start_generate_video(call: types.CallbackQuery, state: FSMContext):
    # Получаем название модели
    model_name = call.data.split("|")[1]

    # Удаляем видео из папки temp/videos, если оно есть
    try:
        stateData = await state.get_data()
        if "video_path" in stateData:
            os.remove(stateData["video_path"])
    except Exception as e:
        logger.error(f"Ошибка при удалении видео из папки temp/videos: {e}")

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение для выбора видео-примеров
    await editMessageOrAnswer(
        call,text.SELECT_VIDEO_TYPE_GENERATION_TEXT.format(model_name, model_name_index),
        reply_markup=video_generation_keyboards.videoWritePromptKeyboard(model_name))


# Обработка нажатия кнопок под видео-примером
async def handle_video_example_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем индекс видео-примера и тип кнопки
    temp = call.data.split("|")
    model_name = temp[1]
    button_type = temp[2]
    user_id = call.from_user.id

    # Получаем название модели и url изображения
    data = await state.get_data()
    image_url = data["images_urls"][model_name]

    # Удаляем сообщение с выбором видео-примера
    # try:
    #     await bot.delete_message(user_id, int(data["select_video_example_message_id"]))
    # except Exception as e:
    #     logger.error(f"Произошла ошибка при удалении сообщения с id {data['select_video_example_message_id']}: {e}")

    # Получаем данные видео-примера по его индексу
    # video_example_data = await getVideoExampleDataByIndex(index)

    # Получаем кастомный промпт, если он есть, а если нет, то берем промпт из видео-примера 
    if "prompt_for_video" in data:
        custom_prompt = data["prompt_for_video"]
    else:
        custom_prompt = None
    # video_example_prompt = custom_prompt if custom_prompt else video_example_data["prompt"]
    video_example_prompt = custom_prompt

    # Получаем путь к видео-примеру
    # video_example_file_id = video_example_data["file_id"]
    # await state.update_data(video_example_file_id=video_example_file_id)

    # Удаляем сообщения с видео-примерами
    # video_examples_messages_ids = data["video_examples_messages_ids"]
    # for message_id in video_examples_messages_ids:
    #     try:
    #         await bot.delete_message(user_id, int(message_id))
    #     except Exception as e:
    #         logger.error(f"Произошла ошибка при удалении сообщения с id {message_id}: {e}")
            
    # Удаляем текущее сообщение
    # try:
    #     await bot.delete_message(user_id, call.message.message_id)
    # except Exception as e:
    #     logger.error(f"Произошла ошибка при удалении сообщения с id {call.message.message_id}: {e}")

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Если кнопка "Написать промпт", то отправляем сообщение для ввода кастомного промпта
    if button_type == "write_prompt":
        # await state.update_data(video_example_file_id=video_example_file_id)
        # await state.update_data(video_example_index=index)
        await state.update_data(model_name=model_name)
        await state.set_state(StartGenerationState.write_prompt_for_video)
        await editMessageOrAnswer(
        call,text.WRITE_PROMPT_FOR_VIDEO_TEXT.format(model_name, model_name_index))
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
    logger.info(f"Сохраняем видео в стейт: {video_path}")
    await state.update_data(video_path=video_path)

    # Удаляем сообщение про генерацию видео
    await bot.delete_message(user_id, message_for_delete.message_id)

    # Отправляем видео
    video = types.FSInputFile(video_path)
    if button_type == "test":
        await call.message.answer_video(video=video, caption=text.GENERATE_TEST_VIDEO_SUCCESS_TEXT.format(model_name), 
        reply_markup=video_generation_keyboards.videoGenerationTypeKeyboard(model_name, False))

    elif button_type == "work":
        await call.message.answer_video(video=video, caption=text.GENERATE_VIDEO_SUCCESS_TEXT.format(model_name, model_name_index), 
        reply_markup=video_generation_keyboards.videoCorrectnessKeyboard(model_name))

# Хедлер для обработки ввода кастомного промпта для видео
async def write_prompt_for_video(message: types.Message, state: FSMContext):
    # Получаем данные
    prompt = message.text
    await state.update_data(prompt_for_video=prompt)
    data = await state.get_data()

    logger.info(f"Получен промпт для генерации видео: {prompt}")

    # Получаем индекс модели
    model_name_index = getModelNameIndex(data["model_name"])

    # Отправляем сообщение
    await state.set_state(None)
    await message.answer(
    text.WRITE_PROMPT_FOR_VIDEO_SUCCESS_TEXT.format(data["model_name"], model_name_index, prompt),
    reply_markup=video_generation_keyboards.videoGenerationTypeKeyboard(data["model_name"], True))


# Обработка нажатия на кнопки корректности видео
async def handle_video_correctness_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем тип кнопки
    temp = call.data.split("|")
    button_type = temp[1]
    model_name = temp[2]

    # Получаем данные
    data = await state.get_data()
    video_path = data["video_path"]

    if button_type == "correct":
        # Удаляем текущее сообщение с видео
        await bot.delete_message(call.message.chat.id, call.message.message_id)

        # Сохраняем видео
        await saveVideo(video_path, model_name, call.message)


# Обработка нажатия на кнопку "📹 Сгенерировать видео из изображения'"
async def start_generateVideoFromImage(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text.SEND_IMAGE_FOR_VIDEO_GENERATION)
    await state.set_state(StartGenerationState.send_image_for_video_generation)


# Обработка присылания изображения для генерации видео и запроса на присылания промпта
async def write_prompt_for_videoGenerationFromImage(message: types.Message, state: FSMContext):
    # Проверяем, есть ли изображение в сообщении
    if not message.photo:
        await message.answer(text.NO_IMAGE_FOR_VIDEO_GENERATION_ERROR_TEXT)
        return

    # Получаем file_id самого большого изображения
    photo = message.photo[-1]
    await state.update_data(image_file_id_for_videoGenerationFromImage=photo.file_id)

    # Просим пользователя ввести промпт для генерации видео
    await state.set_state(None)
    await message.answer(text.WRITE_PROMPT_FOR_VIDEO_GENERATION_FOR_IMAGE_TEXT)
    await state.set_state(StartGenerationState.write_prompt_for_videoGenerationFromImage)


# Хендлер для обработки промпта для генерации видео из изображения
async def handle_prompt_for_videoGenerationFromImage(message: types.Message, state: FSMContext):
    prompt = message.text
    await state.update_data(prompt_for_videoGenerationFromImage=prompt)
    data = await state.get_data()
    image_file_id = data.get("image_file_id_for_videoGenerationFromImage")

    if not image_file_id:
        await message.answer(text.NO_IMAGE_FOR_VIDEO_GENERATION_ERROR_TEXT)
        return

    # Сохраняем сообщение о прогрессе
    await message.answer(text.GENERATE_VIDEO_FROM_IMAGE_PROGRESS_TEXT)

    try:
        # Скачиваем изображение (file_id) и получаем путь к файлу
        # Для этого используем bot.download_file и сохраняем во временную папку
        file = await bot.get_file(image_file_id)
        file_path = file.file_path
        temp_path = f"FocuuusBot/temp/images/{image_file_id}.jpg"
        await bot.download_file(file_path, temp_path)

        # Генерируем видео
        video_path = await retryOperation(generateVideo, 10, 1.5, prompt, None, temp_path)
        await state.update_data(video_path=video_path)

        video = types.FSInputFile(video_path)
        await message.answer_video(video=video, caption=text.GENERATE_VIDEO_FROM_IMAGE_SUCCESS_TEXT)

        # Спрашиваем, в папку какой модели сохранить видео
        await state.set_state(None)
        await message.answer(text.ASK_FOR_MODEL_NAME_FOR_VIDEO_GENERATION_FROM_IMAGE_TEXT)
        await state.set_state(StartGenerationState.ask_for_model_name_for_video_generation_from_image)

        # Удаляем временное изображение
        os.remove(temp_path)
    except Exception as e:
        traceback.print_exc()
        await message.answer(text.GENERATE_VIDEO_ERROR_TEXT.format("", e))
        logger.error(f"Ошибка при генерации видео из изображения: {e}")


# Хендлер для обработки ввода имени модели для сохранения видео
async def handle_model_name_for_video_generation_from_image(message: types.Message, state: FSMContext):
    # Получаем данные по имени модели
    model_name = message.text

    # Если такой модели не существует, то просим ввести другое название
    if not await getDataByModelName(model_name):
        await message.answer(text.MODEL_NOT_FOUND_TEXT)
        return

    stateData = await state.get_data()
    video_path = stateData["video_path"]
    await state.set_state(None)
    await state.update_data(model_name_for_video_generation_from_image=model_name)
    await saveVideo(video_path, model_name, message)


# Добавление обработчиков
def hand_add():
    router.callback_query.register(start_generate_video, lambda call: call.data.startswith("start_generate_video"))

    router.callback_query.register(handle_video_example_buttons, lambda call: call.data.startswith("generate_video"))

    router.message.register(write_prompt_for_video, StateFilter(StartGenerationState.write_prompt_for_video))

    router.callback_query.register(handle_video_correctness_buttons, 
    lambda call: call.data.startswith("video_correctness"))

    router.callback_query.register(
        start_generateVideoFromImage,
        lambda call: call.data == "generateVideoFromImage",
    )

    router.message.register(write_prompt_for_videoGenerationFromImage, 
    StateFilter(StartGenerationState.send_image_for_video_generation))

    router.message.register(handle_prompt_for_videoGenerationFromImage, StateFilter(StartGenerationState.write_prompt_for_videoGenerationFromImage))

    router.message.register(handle_model_name_for_video_generation_from_image, StateFilter(StartGenerationState.ask_for_model_name_for_video_generation_from_image))
