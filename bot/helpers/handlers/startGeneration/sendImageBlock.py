import asyncio
import shutil
import traceback

from aiogram.exceptions import TelegramRetryAfter
from aiogram.fsm.context import FSMContext

import bot.constants as constants
from bot.constants import MULTI_IMAGE_NUMBER
from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    getDataByModelName,
    getModelNameIndex,
)
from bot.InstanceBot import bot
from bot.keyboards import start_generation_keyboards
from bot.logger import logger
from bot.settings import settings
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
    setting_number: str,
    is_test_generation: bool,
    user_id: int,
):
    try:
        # Ограничиваем media_group до 10 элементов (Telegram лимит)
        media_group = media_group[:10]
        media_group_message = await safe_send_media_group(user_id, media_group)
        logger.info(
            f"Media group sent to user_id={user_id}, model_name={model_name}, images_count={len(media_group)}",
        )

        await asyncio.sleep(0.7)
        logger.info(
            f"Slept 0.7s before sending keyboard to user_id={user_id}, model_name={model_name}",
        )

        for idx, media in enumerate(media_group_message):
            data_for_update = {
                "model_name": model_name,
                "image_index": idx + 1,
                "message_id": media.message_id,
            }
            await appendDataToStateArray(
                state,
                "imageGeneration_mediagroup_messages_ids",
                data_for_update,
                unique_keys=("model_name", "image_index"),
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
                    text="Произошла ошибка при отправке изображений, но продолжаем работу...",
                )
        except:
            pass

    try:
        # Получаем данные из стейта
        state_data = await state.get_data()

        # Если номер настройки все, то получаем номер настройки из стейта
        if setting_number == "all":
            setting_number = state_data.get(
                "current_setting_number_for_unique_prompt",
                1,
            )

        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

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
                        setting_number,
                        MULTI_IMAGE_NUMBER,
                        selected_indexes,
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
                await state.update_data(
                    imageGeneration_select_message_id=select_message.message_id
                )
            else:
                reply_markup = start_generation_keyboards.selectImageKeyboard(
                    model_name,
                    setting_number,
                    model_data["json"]["input"]["image_number"],
                )
                await bot.send_message(
                    chat_id=user_id,
                    text=text.SELECT_IMAGE_TEXT.format(
                        model_name,
                        model_name_index,
                    )
                    if not is_test_generation
                    else text.SELECT_TEST_IMAGE_TEXT.format(setting_number),
                    reply_markup=reply_markup
                    if not is_test_generation
                    else start_generation_keyboards.testGenerationImagesKeyboard(
                        setting_number,
                    )
                    if state_data.get("setting_number", 1) != "all"
                    else None,
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

        # Если это тестовая генерация, то удаляем изображения из папки temp/test/ и сами папки
        if is_test_generation and not settings.MOCK_IMAGES_MODE:
            try:
                file_path = f"{constants.TEMP_FOLDER_PATH}/test_{user_id}"
                shutil.rmtree(file_path)
            except Exception as e:
                logger.error(f"Ошибка при удалении временных файлов: {e}")

    except Exception as e:
        raise Exception(f"Произошла ошибка в функции sendImageBlock: {e}")
