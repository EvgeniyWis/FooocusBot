import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from PIL import Image

from bot.config import TEMP_FOLDER_PATH
from bot.helpers import text
from bot.utils.images import image_to_base64
from bot.helpers.generateImages.dataArray import (
    getDataByModelName,
    getModelNameIndex,
    getSettingNumberByModelName,
)
from bot.helpers.generateImages.upscale import upscale_image
from bot.utils.handlers.messages import editMessageOrAnswer


async def process_upscale_image(
    call: types.CallbackQuery,
    state: FSMContext,
    image_index: int,
    model_name: str,
):
    """
    Функция для обработки upscale изображения, обработки процесса в хендлере и сохранения изображения по пути

    Attributes:
        call (types.CallbackQuery): callback-запрос
        state (FSMContext): контекст состояния
        image_index (int): индекс изображения
        model_name (str): название модели
    """
    # Получаем айдишник пользователя
    user_id = call.from_user.id

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение о начале upscale
    upscale_message = await editMessageOrAnswer(
        call,
        text.UPSCALE_IMAGE_PROGRESS_TEXT.format(
            image_index, model_name, model_name_index
        ),
    )

    # Получаем само изображение по пути
    image_path = f"{TEMP_FOLDER_PATH}/{model_name}_{user_id}/{image_index}.jpg"

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    # Если изображение не найдено, то завершаем генерацию
    if not os.path.exists(image_path):
        await editMessageOrAnswer(
            call,
            text.IMAGE_NOT_FOUND_TEXT.format(
                image_index, model_name, model_name_index
            ),
        )
        return

    image = Image.open(image_path)
    image_base64 = image_to_base64(image)

    # Получаем базовую модель
    base_model = data["json"]["input"]["base_model_name"]

    # Получаем номер настройки
    setting_number = getSettingNumberByModelName(model_name)

    # Делаем upscale изображения
    await upscale_image(
        image_base64,
        base_model,
        setting_number,
        state,
        user_id,
        model_name,
        image_index,
        upscale_message.message_id,
    )

    return True
