
import base64

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.factory.iloveapi_task_factory import get_iloveapi_task_factory
from bot.factory.magnific_task_factory import get_magnific_task_factory
from bot.helpers import text
from bot.helpers.handlers.startGeneration.image_processes.process_save_image import (
    process_save_image,
)
from bot.InstanceBot import router
from bot.logger import logger
from bot.utils.handlers.getDataInDictsArray import getDataInDictsArray
from bot.utils.handlers.messages.rate_limiter_for_edit_message import (
    safe_edit_message,
)
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)


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

    # Получаем сервис ILoveAPI
    iloveapi_service = get_iloveapi_task_factory()

    # Запускаем задачу
    try:
        resize_result_response = await iloveapi_service.resize_image(
            file=image_url,
            width=720,
            height="auto",
        )
        resize_result = resize_result_response.content
    except Exception as e:
        await message_for_edit.delete()
        error_text = f"Ошибка при уменьшении разрешения изображения: {e}"
        logger.error(error_text)
        await safe_send_message(
            error_text,
            call.message,
        )
        raise e

    # Изменяем сообщение
    await safe_edit_message(
        message_for_edit,
        text.MAGNIFIC_UPSCALE_TEXT,
    )

    # Получаем сервис Magnific
    magnific_service = get_magnific_task_factory()

    # Преобразуем в base64
    resize_result_base64 = base64.b64encode(resize_result).decode("utf-8")

    # Запускаем upscale
    try:
        magnific_result_url = await magnific_service.upscale_image(
            image=resize_result_base64,
        )
    except Exception as e:
        await message_for_edit.delete()
        error_text = f"Ошибка при Magnific Upscale изображения: {e}"
        logger.error(error_text)
        await safe_send_message(
            error_text,
            call.message,
        )
        raise e

    # Удаляем сообщение о начале upscale
    await message_for_edit.delete()

    # Сохраняем результат
    await process_save_image(
        call,
        state,
        model_name,
        image_index,
        result_url=magnific_result_url,
        name_postfix="_magnific_upscale",
    )


# Добавление обработчиков
def hand_add():
    router.callback_query.register(
        start_magnific_upscale,
        lambda call: call.data.startswith("magnific_upscale"),
    )
