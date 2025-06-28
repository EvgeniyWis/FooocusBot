import traceback

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    getDataArrayBySettingNumber,
)
from bot.helpers.generateImages.generateImageBlock import generateImageBlock
from bot.helpers.generateImages.generateImages import generateImages
from bot.helpers.generateImages.generateImagesByAllSettings import (
    generateImagesByAllSettings,
)
from bot.helpers.handlers.startGeneration.cancelImageGenerationJobs import (
    cancelImageGenerationJobs,
)
from bot.logger import logger
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)


# Функция для генерации изображения в зависимости от настроек
async def generateImagesInHandler(
    prompt: str,
    message: types.Message,
    state: FSMContext,
    user_id: int,
    is_test_generation: bool,
    setting_number: str,
    with_randomizer: bool = False,
):
    # Отправляем сообщение об отмене предыдущих работ
    message_for_edit = await safe_send_message(
        text=text.CANCEL_PREVIOUS_JOBS_TEXT,
        message=message,
    )

    # Отменяем все работы
    await cancelImageGenerationJobs(state)

    # Генерируем изображения
    try:
        state_data = await state.get_data()
        model_indexes_for_generation = state_data.get(
            "model_indexes_for_generation",
            [],
        )

        if is_test_generation:
            if setting_number == "all":
                # Заполнение параметра is_test_generation в вызове функции
                result = await generateImagesByAllSettings(
                    message_for_edit,
                    state,
                    user_id,
                    is_test_generation,
                    prompt,
                )  # Отправляем сообщение о получении промпта
            else:
                await message_for_edit.edit_text(text.GET_PROMPT_SUCCESS_TEXT)

                # Получаем данные для генерации
                dataArray = getDataArrayBySettingNumber(
                    int(setting_number),
                )

                data = dataArray[0]
                result = [
                    await generateImageBlock(
                        data,
                        message_for_edit.message_id,
                        state,
                        user_id,
                        setting_number,
                        prompt,
                        is_test_generation,
                        chat_id=message.chat.id,
                    ),
                ]
        else:
            logger.info(
                f"Получен список моделей для индивидуальной генерации: {model_indexes_for_generation}",
            )

            if setting_number == "all":
                result = await generateImagesByAllSettings(
                    message_for_edit,
                    state,
                    user_id,
                    is_test_generation,
                    prompt,
                    True,
                )
            else:
                await message_for_edit.edit_text(text.GET_PROMPT_SUCCESS_TEXT)

                await message_for_edit.pin()
                result = await generateImages(
                    setting_number,
                    prompt,
                    message_for_edit,
                    state,
                    user_id,
                    is_test_generation,
                    with_randomizer,
                    model_indexes_for_generation,
                )
                await message_for_edit.unpin()

        if not result:
            raise Exception("Произошла ошибка при генерации изображения")
        else:
            state_data = await state.get_data()
            stop_generation = state_data.get("stop_generation", False)

            if not stop_generation and len(model_indexes_for_generation) > 1:
                await safe_send_message(text.GENERATION_SUCCESS_TEXT, message)

    except Exception as e:
        try:
            await message_for_edit.unpin()
        except Exception:
            pass
        logger.error(f"Ошибка при генерации изображения: {e}")
        traceback.print_exc()
        await safe_send_message(text.GENERATION_IMAGE_ERROR_TEXT, message)
        await state.clear()
        raise e
