from aiogram.fsm.context import FSMContext
from ...generateImages.dataArray import getModelNameIndex
from logger import logger
from aiogram import types
import os
from ... import text
from keyboards import video_generation_keyboards
from config import MOCK_MODE

# Функция для отправки сообщения для генерации видео для следующей модели
async def sendNextModelMessage(state: FSMContext, call: types.CallbackQuery, model_name: str = None):
    # Получаем название модели, которая стоит первой в очереди
    stateData = await state.get_data()

    # Если нет изображений, то выходим
    if len(stateData["saved_images_urls"]) == 0:
        return
    
    model_data = stateData["saved_images_urls"][0]
    
    if not model_name:
        model_name = list(model_data.keys())[0]

    # Делаем ссылку
    image_url = model_data[model_name]
    logger.info(f"Изначальный image_url: {image_url}")
    image_id = image_url.split("id=")[1]
    image_url = f"https://drive.google.com/uc?export=view&id={image_id}"

    logger.info(f"Для генерации видео выбрана модель: {model_name} и url изображения: {image_url}")

    await state.update_data(image_url=image_url)

    # Удаляем видео из папки temp/videos, если оно есть
    if not MOCK_MODE:
        stateData = await state.get_data()
        if "video_path" in stateData:
            os.remove(stateData["video_path"])

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение для выбора видео-примеров
    select_video_example_message = await call.message.answer_photo(
        photo=image_url,
        caption=text.SELECT_VIDEO_EXAMPLE_TEXT.format(model_name, model_name_index), 
        reply_markup=video_generation_keyboards.videoGenerationModeKeyboard(model_name))

    await state.update_data(select_video_example_message_id=select_video_example_message.message_id)