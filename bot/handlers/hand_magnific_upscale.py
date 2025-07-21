
from aiogram import types
from aiogram.fsm.context import FSMContext
from FooocusBot.bot.factory.iloveapi_factory import get_iloveapi_factory

from bot.helpers import text
from bot.InstanceBot import router
from bot.logger import logger
from bot.utils.handlers.getDataInDictsArray import getDataInDictsArray
from bot.utils.handlers.messages.rate_limiter_for_edit_message import (
    safe_send_message,
)


# Обработка нажатия на кнопку "🪄 Использовать Magnific Upscaler"
async def start_magnific_upscale(call: types.CallbackQuery, state: FSMContext):
    # Удаляем сообщение о нажатии на кнопку
    await call.message.delete()

    # Отправляем сообщение о начале использования Magnific Upscaler
    await safe_send_message(
        text.START_MAGNIFIC_UPSCALER_TEXT,
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
    iloveapi_service = get_iloveapi_factory()

    # Запускаем задачу
    result = await iloveapi_service.resize_image(
        file=image_url,
        width=720,
        height="auto",
    )

    logger.info(f"Результат обработки ILoveAPI после resize_image: {result}")


# Добавление обработчиков
def hand_add():
    router.callback_query.register(
        start_magnific_upscale,
        lambda call: call.data.startswith("magnific_upscale"),
    )
