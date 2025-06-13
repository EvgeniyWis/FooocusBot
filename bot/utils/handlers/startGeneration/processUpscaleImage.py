from aiogram import types
from aiogram.fsm.context import FSMContext
from utils.generateImages import upscaleImage, base64ToImage, imageToBase64
from utils.generateImages.dataArray import getSettingNumberByModelName, getDataByModelName
from utils.handlers.messages import editMessageOrAnswer
from utils import text
from config import TEMP_FOLDER_PATH
import os
from PIL import Image


async def processUpscaleImage(call: types.CallbackQuery, state: FSMContext, 
    image_index: int, model_name: str, model_name_index: int, user_id: int):
    """
    Функция для обработки upscale изображения, обработки процесса в хендлере и сохранения изображения по пути
    
    Attributes:
        call (types.CallbackQuery): callback-запрос
        state (FSMContext): контекст состояния
        image_index (int): индекс изображения
        model_name (str): название модели
        model_name_index (int): индекс модели
        user_id (int): id пользователя
    """

    await editMessageOrAnswer(
        call,text.UPSCALE_IMAGE_PROGRESS_TEXT.format(image_index, model_name, model_name_index))

    # Получаем само изображение по пути
    image_path = (
        f"{TEMP_FOLDER_PATH}/{model_name}_{user_id}/{image_index}.jpg"
    )

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    # Если изображение не найдено, то завершаем генерацию
    if not os.path.exists(image_path):
        await editMessageOrAnswer(
            call,
            text.IMAGE_NOT_FOUND_TEXT.format(image_index, model_name, model_name_index),
        )
        return

    image = Image.open(image_path)
    image_base64 = imageToBase64(image)

    # Получаем базовую модель
    base_model = data["json"]["input"]["base_model_name"]

    # Получаем номер настройки
    setting_number = getSettingNumberByModelName(model_name)

    # Делаем upscale изображения
    images_output_base64 = await upscaleImage(image_base64, base_model, setting_number, state, user_id)

    # Сохраняем изображения по этому же пути
    await base64ToImage(
        images_output_base64,
        model_name,
        int(image_index) - 1,
        user_id,
        False,
                )