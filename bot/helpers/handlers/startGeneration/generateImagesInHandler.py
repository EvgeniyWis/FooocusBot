import traceback

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.logger import logger
from bot.helpers import text
from bot.helpers.generateImages import (
    generateImageBlock,
    generateImages,
    generateImagesByAllSettings,
)
from bot.helpers.generateImages.dataArray import (
    getDataArrayBySettingNumber,
)
from bot.helpers.handlers.startGeneration.cancelImageGenerationJobs import (
    cancelImageGenerationJobs,
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
    message_for_edit = await message.answer(text.CANCEL_PREVIOUS_JOBS_TEXT)

    # Отменяем все работы
    await cancelImageGenerationJobs(state)

    # Генерируем изображения
    try:
        if is_test_generation:
            if setting_number == "all":
                # Заполнение параметра is_test_generation в вызове функции
                result = await generateImagesByAllSettings(
                    message_for_edit,
                    state,
                    user_id,
                    is_test_generation,
                )  # Отправляем сообщение о получении промпта
            else:
                await message_for_edit.edit_text(text.GET_PROMPT_SUCCESS_TEXT)

                # Получаем данные для генерации
                dataArray = getDataArrayBySettingNumber(
                    int(setting_number),
                )

                # Прибавляем корневой промпт
                json = dataArray[0]["json"].copy()
                json["input"]["prompt"] += " " + prompt

                model_name = dataArray[0]["model_name"]
                result = [
                    await generateImageBlock(
                        json,
                        model_name,
                        message_for_edit.message_id,
                        state,
                        user_id,
                        setting_number,
                        is_test_generation,
                        chat_id=message.chat.id,
                    ),
                ]
        else:
            stateData = await state.get_data()
            model_indexes_for_generation = stateData.get(
                "model_indexes_for_generation", []
            )
            logger.info(
                f"Получен список моделей для индивидуальной генерации: {model_indexes_for_generation}"
            )

            if setting_number == "all":
                result = await generateImagesByAllSettings(
                    message_for_edit,
                    state,
                    user_id,
                    is_test_generation,
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
            stateData = await state.get_data()
            stop_generation = stateData.get("stop_generation", False)

            if not stop_generation and len(model_indexes_for_generation) > 1:
                await message.answer(text.GENERATION_SUCCESS_TEXT)

    except Exception as e:
        try:
            await message_for_edit.unpin()
        except Exception:
            pass
        logger.error(f"Ошибка при генерации изображения: {e}")
        traceback.print_exc()
        await message.answer(text.GENERATION_IMAGE_ERROR_TEXT)
        await state.clear()
        raise e
