import asyncio
import traceback

from aiogram.exceptions import TelegramRetryAfter
from aiogram.fsm.context import FSMContext

from bot.constants import MULTI_IMAGE_NUMBER
from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    get_model_index_by_model_name,
    getDataByModelName,
)
from bot.InstanceBot import bot
from bot.keyboards import start_generation_keyboards
from bot.logger import logger
from bot.utils.handlers import (
    appendDataToStateArray,
)
from bot.utils.handlers.messages import (
    safe_send_media_group,
)


# Функция для отправки сообщения со сгенерируемыми изображениями
async def sendImageBlock(
    state: FSMContext,
    media_group: list,
    model_name: str,
    group_number: str,
    user_id: int,
    job_id: str,
):
    try:
        # Ограничиваем media_group до 10 элементов (Telegram лимит)
        media_group = media_group[:10]
        media_group_message = await safe_send_media_group(user_id, media_group)
        if media_group_message is None:
            media_group_message = await safe_send_media_group(user_id, media_group)

        if media_group_message is None:
            logger.error(
                "media_group_message is None! Возможно, не удалось отправить медиагруппу."
            )
            raise Exception("media_group_message is None! Возможно, не удалось отправить медиагруппу.")

        if not hasattr(media_group_message, "__iter__"):
            logger.error(
                f"media_group_message не итерируемый объект: {type(media_group_message)}"
            )
            await bot.send_message(
                chat_id=user_id,
                text="Произошла ошибка при отправке изображений! (media_group_message не итерируемый)",
            )
            return
        logger.info(
            f"Media group sent to user_id={user_id}, model_name={model_name}, images_count={len(media_group)}",
        )

        await asyncio.sleep(0.7)
        logger.info(
            f"Slept 0.7s before sending keyboard to user_id={user_id}, model_name={model_name}",
        )

        for i, message in enumerate(media_group_message):
            await appendDataToStateArray(
                state,
                "media_messages",
                {
                    "model_name": model_name,
                    "image_index": i,
                    "job_id": job_id,
                    "message_id": message.message_id,
                    "type": "media",
                },
                unique_keys=("model_name", "image_index", "job_id"),
            )

    except Exception as e:
        traceback.print_exc()
        logger.error(f"Ошибка при отправке медиагруппы: {e}")
        try:
            if isinstance(e, TelegramRetryAfter):
                await bot.send_message(
                    chat_id=user_id,
                    text=f"Превышен лимит отправки сообщений. Пожалуйста, подождите {e.retry_after} секунд и попробуйте снова.",
                )
            else:
                await bot.send_message(
                    chat_id=user_id,
                    text=f"Произошла ошибка при отправке изображений! Текст ошибки: {e}",
                )
        except:
            pass

    try:
        # Получаем данные из стейта
        state_data = await state.get_data()

        # Если номер группы все, то получаем номер группы из стейта
        if group_number == "all":
            group_number = state_data.get(
                "current_group_number_for_unique_prompt",
                1,
            )

        # Получаем индекс модели
        model_name_index = get_model_index_by_model_name(model_name)

        # Получаем данные модели
        model_data = await getDataByModelName(model_name)

        # Отправляем клавиатуру для выбора изображения
        try:
            multi_select_mode = state_data.get("multi_select_mode", False)
            selected_indexes = state_data.get("selected_indexes", [])
            if multi_select_mode:
                reply_markup = (
                    start_generation_keyboards.selectMultiImageKeyboard(
                        model_name,
                        group_number,
                        MULTI_IMAGE_NUMBER,
                        selected_indexes,
                        job_id,
                    )
                )
                select_message = await bot.send_message(
                    chat_id=user_id,
                    text=text.SELECT_SOME_IMAGES_TEXT.format(
                        model_name,
                        model_name_index,
                    ),
                    reply_markup=reply_markup,
                )
                await appendDataToStateArray(
                    state,
                    "imageGeneration_mediagroup_messages_ids",
                    {
                        "model_name": model_name,
                        "generation_id": job_id,
                        "message_id": select_message.message_id,
                        "type": "keyboard",
                    },
                    unique_keys=("model_name", "generation_id", "type"),
                )
            else:
                reply_markup = start_generation_keyboards.selectImageKeyboard(
                    model_name,
                    group_number,
                    model_data["json"]["input"]["image_number"],
                    job_id,
                )
                await bot.send_message(
                    chat_id=user_id,
                    text=text.SELECT_IMAGE_TEXT.format(
                        model_name,
                        model_name_index,
                    ),
                    reply_markup=reply_markup,
                )
            logger.info(
                f"Keyboard sent to user_id={user_id}, model_name={model_name}",
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения с клавиатурой: {e}")
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text="Произошла ошибка при отправке клавиатуры...",
                )
            except:
                pass
    except Exception as e:
        raise Exception(f"Произошла ошибка в функции sendImageBlock: {e}")
