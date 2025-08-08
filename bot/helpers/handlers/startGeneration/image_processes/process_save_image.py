import os
import traceback
from datetime import datetime

import pytz
from aiogram import types
from aiogram.fsm.context import FSMContext
from constants import FACEFUSION_TEMP_IMAGES_FOLDER_PATH
from utils.handlers.messages.rate_limiter_for_send_photo import safe_send_photo

from bot.assets.mocks.links import (
    MOCK_LINK_FOR_SAVE_IMAGE,
)
from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    get_model_index_by_model_name,
    getDataByModelName,
)
from bot.helpers.jobs.get_job_id_by_model_name import get_job_id_by_model_name
from bot.keyboards import video_generation_keyboards
from bot.logger import logger
from bot.settings import settings
from bot.utils.googleDrive.files import convertDriveLink
from bot.utils.googleDrive.files.saveFile import saveFile
from bot.utils.googleDrive.folders.getFolderDataByID import getFolderDataByID
from bot.utils.handlers import appendDataToStateArray
from bot.utils.handlers.messages import editMessageOrAnswer


async def process_save_image(
    call: types.CallbackQuery,
    state: FSMContext,
    model_name: str,
    image_index: int,
    result_path: str = None,
    result_url: str = None,
    name_postfix: str = None,
    kb_with_magnific_upscale: bool = True,
    model_key: str = None,
) -> str:
    """
    Обрабатывает сохранение изображения после этапа замены лица.

    Args:
        - call: CallbackQuery, объект вызова
        - state: FSMContext, контекст состояния
        - model_name: str, название модели
        - result_path: str, путь к результату, полученный с замены лица
        - result_url: str, URL результата, полученный с замены лица
        - image_index: int, индекс изображения
        - kb_with_magnific_upscale: bool, флаг для отображения клавиатуры с Magnific Upscaler

    Returns:
        - direct_url: ссылка на сохранённое изображение
    """

    # Получаем данные пользователя
    user_id = call.from_user.id
    # Получаем job_id для текущей модели
    job_id = await get_job_id_by_model_name(state, model_name, model_key)
    temp_user_dir = FACEFUSION_TEMP_IMAGES_FOLDER_PATH / f"{job_id}"
    logger.info(
        f"[save] START: dir={os.listdir(temp_user_dir) if temp_user_dir.exists() else 'NO_DIR'}",
    )

    # Получаем индекс модели
    model_name_index = get_model_index_by_model_name(model_name)

    # Меняем текст на сообщении
    saving_progress_message = await editMessageOrAnswer(
        call,
        text.SAVE_IMAGE_PROGRESS_TEXT.format(model_name, model_name_index),
    )

    # Получаем данные модели
    model_data = await getDataByModelName(model_name)

    # Сохраняем изображение
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.now(tz).strftime("%Y-%m-%d")

    if not settings.MOCK_IMAGES_MODE:
        state_data = await state.get_data()
        multi_select_mode = bool(state_data.get("multi_select_mode", False))

        link = await saveFile(
            file_path=result_path,
            file_url=result_url,
            user_id=user_id,
            folder_name=model_name,
            initial_folder_id=model_data["picture_folder_id"],
            current_date=now,
            image_index=image_index if multi_select_mode else None,
            name_postfix=name_postfix,
        )
    else:
        link = MOCK_LINK_FOR_SAVE_IMAGE

    # Конвертируем ссылку в прямую ссылку для скачивания
    direct_url = convertDriveLink(link)

    data_for_update = {
        "model_name": model_name,
        "image_index": image_index,
        "direct_url": direct_url,
    }
    state_data = await state.get_data()
    saved_images_urls = state_data.get("saved_images_urls", [])
    
    logger.info(f"Сохраняем данные для ({model_name}, {image_index}): {data_for_update}")
    logger.info(f"Текущий массив saved_images_urls: {saved_images_urls}")
    
    updated = False
    for idx, obj in enumerate(saved_images_urls):
        if obj["model_name"] == model_name and obj["image_index"] == image_index:
            logger.info(f"Обновляем существующую запись для ({model_name}, {image_index})")
            saved_images_urls[idx] = data_for_update
            updated = True
            break
    if not updated:
        logger.info(f"Добавляем новую запись для ({model_name}, {image_index})")
        saved_images_urls.append(data_for_update)
    
    await state.update_data(saved_images_urls=saved_images_urls)
    logger.info(f"Обновленный массив saved_images_urls: {saved_images_urls}")

    if not link:
        traceback.print_exc()
        data_for_update = {
            "model_name": model_name,
            "image_index": image_index,
        }
        await appendDataToStateArray(
            state,
            "save_image_errors",
            data_for_update,
        )
        await editMessageOrAnswer(
            call,
            text.SAVE_FILE_ERROR_TEXT.format(model_name, model_name_index),
        )
        return

    # Получаем данные родительской папки
    folder = await getFolderDataByID(model_data["picture_folder_id"])
    parent_folder_id = folder["parents"][0]
    parent_folder = await getFolderDataByID(parent_folder_id)

    logger.info(
        f"Данные папки по id {model_data['picture_folder_id']}: {folder}",
    )
    logger.info(
        f"Сохранили ссылку для ({model_name}, {image_index}): {direct_url}",
    )

    # Отправляем сообщение о сохранении изображения
    logger.info(
        f"Отправляем сообщение о сохранении изображения: {direct_url}",
    )

    message_text = (
        text.SAVE_IMAGES_SUCCESS_TEXT_WITH_MAGNIFIC_UPSCALER
        if not kb_with_magnific_upscale
        else text.SAVE_IMAGES_SUCCESS_TEXT
    )

    # Сначала пытаемся отправить локальный файл, если он доступен
    photo_source = None
    if result_path and os.path.exists(result_path):
        photo_source = result_path
        logger.info(f"Используем локальный файл для отправки: {result_path}")
    else:
        photo_source = direct_url
        logger.info(f"Используем URL для отправки: {direct_url}")

    message_with_saved_image = await safe_send_photo(
        photo=photo_source,
        message=call,
        caption=message_text.format(
            link,
            model_name,
            parent_folder["webViewLink"],
            model_name_index,
        ),
        reply_markup=video_generation_keyboards.generateVideoKeyboard(
            model_name,
            image_index=image_index,
            with_magnific_upscale=kb_with_magnific_upscale,
        ),
    )

    # Проверяем, что сообщение было отправлено успешно
    if message_with_saved_image is None:
        logger.error(f"Не удалось отправить фото с источником: {photo_source}")
        
        # Если использовали локальный файл, попробуем URL
        reply_markup = video_generation_keyboards.generateVideoKeyboard(
            model_name,
            image_index=image_index,
            with_magnific_upscale=kb_with_magnific_upscale,
        )
        if photo_source == result_path and direct_url != result_path:
            logger.info("Пробуем отправить через URL как альтернативу")
            message_with_saved_image = await safe_send_photo(
                photo=direct_url,
                message=call,
                caption=message_text.format(
                    link,
                    model_name,
                    parent_folder["webViewLink"],
                    model_name_index,
                ),
                reply_markup=reply_markup,
            )
        
        # Если все еще не удалось, отправляем текстовое сообщение
        if message_with_saved_image is None:
            await editMessageOrAnswer(
                call,
                f"Изображение сохранено, но не удалось отправить фото.\nСсылка: {link}",
                reply_markup=reply_markup,
            )
            return direct_url

    data_for_update = {
        "model_name": model_name,
        "image_index": image_index,
        "message_id": message_with_saved_image.message_id,
    }
    await appendDataToStateArray(
        state,
        "messages_with_saved_images",
        data_for_update,
        unique_keys=("model_name", "image_index"),
    )
    # Удаляем сообщение о сохранении изображения
    try:
        await saving_progress_message.delete()
    except Exception as e:
        logger.error(f"Произошла ошибка при удалении сообщения: {e}")

    logger.info(
        f"[save] END: dir={os.listdir(temp_user_dir) if temp_user_dir.exists() else 'NO_DIR'}",
    )

    return direct_url
