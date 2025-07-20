
from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.helpers import text
from bot.InstanceBot import router
from bot.logger import logger
from bot.utils.handlers.getDataInDictsArray import getDataInDictsArray
from bot.utils.handlers.messages.rate_limiter_for_edit_message import (
    safe_edit_message,
)


# Обработка нажатия на кнопку "🪄 Использовать Magnific Upscaler"
async def start_magnific_upscale(call: types.CallbackQuery, state: FSMContext):
    # Отправляем сообщение о начале использования Magnific Upscaler
    await safe_edit_message(
        text.START_MAGNIFIC_UPSCALER_TEXT,
        call.message,
    )

    # Получаем данные
    model_name = call.data.split("|")[1]
    image_index = call.data.split("|")[2]

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


# Добавление обработчиков
def hand_add():
    router.callback_query.register(
        start_magnific_upscale,
        lambda call: call.data.startswith("magnific_upscale"),
    )
