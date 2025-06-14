import shutil

from aiogram.exceptions import TelegramRetryAfter
from aiogram.fsm.context import FSMContext

from bot.config import MOCK_MODE, TEMP_FOLDER_PATH
from bot.InstanceBot import bot
from bot.keyboards import start_generation_keyboards
from bot.logger import logger
from bot.utils import text
from bot.utils.generateImages.dataArray import (
    getDataByModelName,
    getModelNameIndex,
)
from bot.utils.handlers import (
    appendDataToStateArray,
)
from bot.utils.handlers.startGeneration.rate_limiter_for_send_media_group import (
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
        # Отправляем изображения с механизмом повторных попыток и глобальным rate limiter
        media_group_message = await safe_send_media_group(user_id, media_group)

        # Сохраняем их в стейт
        dataForUpdate = {
            f"{model_name}": [
                media.message_id for media in media_group_message
            ],
        }
        await appendDataToStateArray(
            state,
            "imageGeneration_mediagroup_messages_ids",
            dataForUpdate,
        )
    except Exception as e:
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
        stateData = await state.get_data()

        # Если номер настройки все, то получаем номер настройки из стейта
        if setting_number == "all":
            setting_number = stateData.get(
                "current_setting_number_for_unique_prompt",
                1,
            )

        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

        # Получаем данные модели
        model_data = await getDataByModelName(model_name)

        # Отправляем клавиатуру для выбора изображения
        try:
            await bot.send_message(
                chat_id=user_id,
                text=text.SELECT_IMAGE_TEXT.format(
                    model_name,
                    model_name_index,
                )
                if not is_test_generation
                else text.SELECT_TEST_IMAGE_TEXT.format(setting_number),
                reply_markup=start_generation_keyboards.selectImageKeyboard(
                    model_name,
                    setting_number,
                    model_data["json"]["input"]["image_number"],
                )
                if not is_test_generation
                else start_generation_keyboards.testGenerationImagesKeyboard(
                    setting_number,
                )
                if stateData.get("setting_number", 1) != "all"
                else None,
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
        if is_test_generation and not MOCK_MODE:
            try:
                file_path = f"{TEMP_FOLDER_PATH}/test_{user_id}"
                shutil.rmtree(file_path)
            except Exception as e:
                logger.error(f"Ошибка при удалении временных файлов: {e}")

    except Exception as e:
        raise Exception(f"Произошла ошибка в функции sendImageBlock: {e}")
