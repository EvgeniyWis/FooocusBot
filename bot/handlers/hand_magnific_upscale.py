

import os

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.factory.magnific_task_factory import get_magnific_task_factory
from bot.helpers import text
from bot.helpers.handlers.startGeneration.image_processes.process_save_image import (
    process_save_image,
)
from bot.InstanceBot import magnific_upscale_router
from bot.logger import logger
from bot.utils.file_validation import (
    FileValidationError,
    validate_image_for_magnific,
)
from bot.utils.googleDrive.files import downloadFromGoogleDrive
from bot.utils.googleDrive.files.getGoogleDriveFileID import (
    getGoogleDriveFileID,
)
from bot.utils.handlers.getDataInDictsArray import getDataInDictsArray
from bot.utils.handlers.messages.rate_limiter_for_edit_message import (
    safe_edit_message,
)
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)
from bot.utils.images.resize_image import resize_image


# Обработка нажатия на кнопку "🪄 Использовать Magnific Upscaler"
async def start_magnific_upscale(call: types.CallbackQuery, state: FSMContext):
    # Удаляем сообщение о нажатии на кнопку
    await call.message.delete()

    # Отправляем сообщение о начале использования Magnific Upscaler
    message_for_edit = await safe_send_message(
        text.RESIZE_IMAGE_TEXT,
        call,
    )

    # Получаем данные
    model_name = call.data.split("|")[1]
    image_index = int(call.data.split("|")[2])

    # Получаем данные из стейта
    state_data = await state.get_data()
    saved_images_urls = state_data.get("saved_images_urls", [])

    logger.info(
        f"Произвожу поиск изображения по индексу {image_index} и имени модели {model_name} в массиве: {saved_images_urls}",
    )

    image_url = await getDataInDictsArray(
        saved_images_urls,
        model_name,
        image_index,
    )

    if not image_url:
        await safe_send_message(
            "Ошибка: не удалось найти URL изображения",
            call.message,
        )
        return

    logger.info(f"URL изображения для Magnific Upscaler: {image_url}")

    # Скачиваем изображение по url
    image_id = getGoogleDriveFileID(image_url)
    image_path = await downloadFromGoogleDrive(image_id)
    
    # Уменьшаем разрешение изображения
    await resize_image(image_path, 720, 1280)

    logger.info(f"Изображение успешно уменьшено до размера 720x1280: {image_path}")
    
    # Проверяем, что файл существует
    if not os.path.exists(image_path):
        error_text = f"❌ Файл не найден после изменения размера: {image_path}"
        logger.error(error_text)
        await safe_edit_message(
            message_for_edit,
            error_text
        )
        return
    
    # Изменяем сообщение
    await safe_edit_message(
        message_for_edit,
        text.MAGNIFIC_UPSCALE_TEXT,
    )

    # Получаем сервис Magnific
    magnific_service = get_magnific_task_factory()

    # Валидируем файл и получаем base64 строку
    try:
        width, height, resize_result_base64 = validate_image_for_magnific(image_path)
        logger.info(f"Файл успешно валидирован: {width}x{height}")
    except FileValidationError as e:
        await safe_edit_message(
            message_for_edit,
            f"❌ Ошибка валидации файла: {e}"
        )
        return

    # Запускаем upscale
    try:
        magnific_result_url = await magnific_service.upscale_image(
            image=resize_result_base64,
            optimized_for="standard",
            creativity=-8,
            hdr=8,
            resemblance=-10,
            fractality=6,
            engine="magnific_sharpy",
            scale_factor="2x",
        )
    except Exception as e:
        # Безопасно удаляем сообщение
        try:
            await message_for_edit.delete()
        except Exception as delete_error:
            logger.warning(f"Не удалось удалить сообщение: {delete_error}")
        
        error_text = f"Ошибка при Magnific Upscale изображения: {e}"
        logger.error(error_text)
        await safe_send_message(
            error_text,
            call.message,
        )
        return  # Возвращаемся вместо raise, чтобы избежать повторной обработки ошибки

    # Удаляем сообщение о начале upscale
    await message_for_edit.delete()

    # Сохраняем результат
    await process_save_image(
        call,
        state,
        model_name,
        image_index,
        result_url=magnific_result_url,
        name_postfix="magnific_upscale",
        kb_with_magnific_upscale=False,
    )

    # Удаляем временный файл
    try:
        os.remove(image_path)
    except Exception as e:
        logger.error(f"Ошибка при удалении временного файла: {e}")


# Добавление обработчиков
def hand_add():
    magnific_upscale_router.callback_query.register(
        start_magnific_upscale,
        lambda call: call.data.startswith("magnific_upscale"),
    )
