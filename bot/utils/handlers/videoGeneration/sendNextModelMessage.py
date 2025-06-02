import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from config import MOCK_MODE
from keyboards import video_generation_keyboards
from logger import logger

from ... import text
from ...generateImages.dataArray import getModelNameIndex


# Функция для отправки сообщения для генерации видео для следующей модели
async def sendNextModelMessage(state: FSMContext, call: types.CallbackQuery, model_name: str = None):
    # Получаем название модели, которая стоит первой в очереди
    stateData = await state.get_data()

    if not model_name:
        # Создаем новый список со всеми значениями
        images_urls = stateData["images_urls_for_videos"].copy()
    else:
        # Создаем новый список со всеми значениями
        images_urls = stateData["saved_images_urls"].copy()

    # Если текущее изображение последнее, то выходим
    logger.info(f"Сохранённые изображения на данный момент (отправка следующей модели): {images_urls} Текущая модель: {model_name}")
    if len(images_urls) == 0:
        return

    if not model_name:
        model_data = images_urls[0]

        # Удаляем первый элемент из списка
        images_urls.pop(0)

        # Сохраняем стейт
        await state.update_data(images_urls_for_videos=images_urls)

        model_name = list(model_data.keys())[0]

    else:
        model_data = next((item for item in images_urls if model_name in item), None)

        # Удаляем этот элемент из списка
        images_urls = [item for item in images_urls if model_name not in item]

        # Сохраняем стейт
        await state.update_data(saved_images_urls=images_urls)

    # Делаем ссылку
    image_url = model_data[model_name]
    logger.info(f"Изначальный image_url: {image_url}")
    image_id = image_url.split("id=")[1]
    image_url = f"https://drive.google.com/uc?export=view&id={image_id}"

    logger.info(f"Для генерации видео выбрана модель: {model_name} и url изображения: {image_url}")

    await state.update_data(image_url=image_url)

    # Удаляем видео из папки temp/videos, если оно есть
    if not MOCK_MODE:
        try:
            if stateData["generated_video_paths"]:
                os.remove(stateData["generated_video_paths"][0]["video_path"])
        except Exception as e:
            logger.error(f"Ошибка при удалении видео из папки temp/videos: {e}")

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение для выбора видео-примеров
    select_video_example_message = await call.message.answer_photo(
        photo=image_url,
        caption=text.SELECT_VIDEO_EXAMPLE_TEXT.format(model_name, model_name_index),
        reply_markup=video_generation_keyboards.videoGenerationModeKeyboard(model_name))

    await state.update_data(select_video_example_message_id=select_video_example_message.message_id)
