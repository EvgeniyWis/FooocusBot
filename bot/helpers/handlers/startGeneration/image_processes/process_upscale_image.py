import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from PIL import Image

from bot.constants import TEMP_FOLDER_PATH
from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    getDataByModelName,
    getModelNameIndex,
    getSettingNumberByModelName,
)
from bot.helpers.generateImages.upscale import upscale_image
from bot.helpers.handlers.messages import send_progress_message
from bot.utils.handlers import (
    deleteDataFromStateArray,
)
from bot.logger import logger
from bot.utils.handlers.messages import editMessageOrAnswer
from bot.utils.images import image_to_base64


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

    image_path = (
        TEMP_FOLDER_PATH / f"{model_name}_{user_id}" / f"{image_index}.jpg"
    )
    temp_user_dir = TEMP_FOLDER_PATH / f"{model_name}_{user_id}"
    logger.info(
        f"[upscale] START: {image_path} exists={os.path.exists(image_path)} | dir={os.listdir(temp_user_dir) if temp_user_dir.exists() else 'NO_DIR'}",
    )

    # Отправляем сообщение о начале upscale
    upscale_message_id = await send_progress_message(
        state,
        "upscale_progress_messages",
        model_name,
        call.message,
        text.UPSCALE_IMAGE_PROGRESS_TEXT.format(image_index, model_name, model_name_index),
        call.message.message_id,
    )

    if temp_user_dir.exists():
        logger.info(
            f"[process_upscale_image] Содержимое папки {temp_user_dir}: {os.listdir(temp_user_dir)}",
        )
    else:
        logger.warning(
            f"[process_upscale_image] Папка {temp_user_dir} не существует!",
        )

    logger.info(
        f"[process_upscale_image] Проверка файла: {image_path} exists={os.path.exists(image_path)}",
    )

    data = await getDataByModelName(model_name)

    if not os.path.exists(image_path):
        logger.error(
            f"[process_upscale_image] Файл не найден для апскейла: {image_path} (model={model_name}, image_index={image_index}, user_id={user_id})",
        )
        await editMessageOrAnswer(
            call,
            f"❌ Изображение для апскейла не найдено! (model={model_name}, image_index={image_index})",
        )
        return None

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
        upscale_message_id,
    )

    # Удаляем из стейта данные о начале upscale
    await deleteDataFromStateArray(
        state,
        "upscale_progress_messages",
        model_name,
        "model_name",
    )
    logger.info(
        f"[upscale] END: {image_path} exists={os.path.exists(image_path)} | dir={os.listdir(temp_user_dir) if temp_user_dir.exists() else 'NO_DIR'}",
    )

    return True
