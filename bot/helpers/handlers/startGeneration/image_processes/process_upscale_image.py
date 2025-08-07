import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from PIL import Image, UnidentifiedImageError

from bot.constants import TEMP_FOLDER_PATH
from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    get_model_index_by_model_name,
    getDataByModelName,
)
from bot.helpers.generateImages.upscale import (
    second_upscale_image,
    upscale_image,
)
from bot.helpers.handlers.messages import send_progress_message
from bot.helpers.jobs.get_job_id_by_model_name import get_job_id_by_model_name
from bot.logger import logger
from bot.utils.handlers import (
    deleteDataFromStateArray,
)
from bot.utils.handlers.messages import editMessageOrAnswer
from bot.utils.images import image_to_base64, is_valid_image
from bot.utils.retryOperation import retryOperation


async def check_file_exists(image_path: str) -> bool:
    """
    Проверяет существование файла
    """
    exists = os.path.exists(str(image_path))
    logger.info(f"[check_file_exists] Проверяем файл: {image_path}, exists={exists}")
    if not exists:
        raise FileNotFoundError(f"Файл не найден: {image_path}")
    return True


async def process_upscale_image(
    call: types.CallbackQuery,
    state: FSMContext,
    image_index: int,
    model_name: str,
    is_second: bool = False,
    model_key: str = None,
):
    """
    Функция для обработки upscale изображения, обработки процесса в хендлере и сохранения изображения по пути

    Attributes:
        call (types.CallbackQuery): callback-запрос
        state (FSMContext): контекст состояния
        image_index (int): индекс изображения
        model_name (str): название модели
        is_second (bool): флаг, что это второй upscale
    """
    # Получаем айдишник пользователя
    user_id = call.from_user.id

    # Получаем индекс модели
    model_name_index = get_model_index_by_model_name(model_name)

    # Получаем job_id для текущей модели
    job_id = await get_job_id_by_model_name(state, model_name, model_key)
    image_path = (
        TEMP_FOLDER_PATH / f"{job_id}" / f"{image_index}.jpg"
    )
    temp_user_dir = TEMP_FOLDER_PATH / f"{job_id}"
    log_prefix = "second_upscale" if is_second else "upscale"
    
    # Добавляем подробное логирование в начале
    logger.info(f"[process_upscale_image] ENTRY: is_second={is_second} (type: {type(is_second)}), model_name={model_name}, image_index={image_index}, user_id={user_id}")
    logger.info(f"[process_upscale_image] job_id={job_id}, image_path={image_path}")
    logger.info(f"[process_upscale_image] temp_user_dir={temp_user_dir}, exists={temp_user_dir.exists()}")
    logger.info(f"[process_upscale_image] log_prefix={log_prefix} (is_second={is_second})")
    
    if temp_user_dir.exists():
        logger.info(f"[process_upscale_image] Содержимое папки {temp_user_dir}: {os.listdir(temp_user_dir)}")
    else:
        logger.warning(f"[process_upscale_image] Папка {temp_user_dir} не существует!")
    
    logger.info(
        f"[{log_prefix}] START: {image_path} exists={os.path.exists(image_path)} | dir={os.listdir(temp_user_dir) if temp_user_dir.exists() else 'NO_DIR'}",
    )

    # Отправляем сообщение о начале upscale
    message_text = text.UPSCALE_IMAGE_PROGRESS_TEXT.format(image_index, model_name, model_name_index) if not is_second else text.SECOND_UPSCALE_IMAGE_PROGRESS_TEXT.format(image_index, model_name, model_name_index)
    upscale_message_id = await send_progress_message(
        state,
        f"{log_prefix}_progress_messages",
        model_name,
        call.message,
        message_text,
        image_index,
        call.message.message_id,
    )

    logger.info(f"TEMP_FOLDER_PATH: {TEMP_FOLDER_PATH} | type: {type(TEMP_FOLDER_PATH)}")
    logger.info(f"image_path: {image_path} | type: {type(image_path)} | exists: {os.path.exists(str(image_path))}")
    logger.info(f"str(image_path): {str(image_path)}")

    logger.info(
        f"[process_{log_prefix}_image] Проверка файла: {image_path} exists={os.path.exists(str(image_path))}",
    )

    data = await getDataByModelName(model_name)

    # Проверяем существование файла с повторными попытками
    try:
        await retryOperation(
            check_file_exists,
            3,  # max_attempts
            10,  # delay в секундах
            str(image_path)
        )
    except Exception:
        logger.error(
            f"[process_{log_prefix}_image] Файл не найден после всех попыток: {image_path} (model={model_name}, image_index={image_index}, user_id={user_id})",
        )
        await editMessageOrAnswer(
            call,
            f"❌ Изображение для апскейла не найдено! (model={model_name}, image_index={image_index})",
        )
        raise Exception(f"Файл не найден для апскейла: {image_path} (model={model_name}, image_index={image_index}, user_id={user_id})")

    try:
        image = Image.open(image_path)
        
        # Проверяем валидность изображения перед обработкой
        if not is_valid_image(image):
            logger.error(
                f"[process_{log_prefix}_image] Изображение повреждено или недопустимо: {image_path}"
            )
            await editMessageOrAnswer(
                call,
                f"❌ Изображение повреждено или имеет недопустимый формат! (model={model_name}, image_index={image_index})",
            )
            return None
            
        image_base64 = image_to_base64(image)
    except (OSError, ValueError, UnidentifiedImageError) as e:
        logger.error(
            f"[process_{log_prefix}_image] Ошибка при обработке изображения {image_path}: {e}"
        )
        await editMessageOrAnswer(
            call,
            f"❌ Ошибка при обработке изображения! Возможно, файл поврежден. (model={model_name}, image_index={image_index})",
        )
        return None

    # Получаем базовую модель
    base_model = data["json"]["input"]["base_model_name"]

    # Делаем upscale изображения
    if is_second:
        await second_upscale_image(
            str(image_path),
            model_name,
            image_index,
            user_id,
            state,
        )
    else:
        await upscale_image(
            image_base64,
            base_model,
            state,
            user_id,
            model_name,
            image_index,
            upscale_message_id,
        )

    # Удаляем из стейта данные о начале upscale
    await deleteDataFromStateArray(
        state,
        f"{log_prefix}_progress_messages",
        model_name,
        "model_name",
    )
    logger.info(
        f"[{log_prefix}] END: {image_path} exists={os.path.exists(str(image_path))} | dir={os.listdir(temp_user_dir) if temp_user_dir.exists() else 'NO_DIR'}",
    )

    return True
