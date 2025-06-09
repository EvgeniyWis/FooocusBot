import asyncio
import traceback

from aiogram import types
from aiogram.fsm.context import FSMContext
from logger import logger

from ... import text
from ...generateImages import (
    generateImageBlock,
    generateImages,
    generateImagesByAllSettings,
)
from ...generateImages.dataArray import (
    getDataArrayBySettingNumber,
)
import asyncio



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
    # Генерируем изображения
    try:
        # Добавлена проверка на None для переменной message перед использованием
        if message is None:
            raise ValueError("message не может быть None")

        # Инициализация переменной message_for_edit перед её использованием
        message_for_edit = None

        if is_test_generation:
            if setting_number == "all":
                # Заполнение параметра is_test_generation в вызове функции
                result = await generateImagesByAllSettings(
                    message,
                    state,
                    user_id,
                    is_test_generation,
                )  # Отправляем сообщение о получении промпта
            else:
                # Инициализация переменной message_for_edit перед её использованием
                message_for_edit = await message.answer(
                    text.GET_PROMPT_SUCCESS_TEXT,
                )
                # Получаем данные для генерации
                dataArray = await getDataArrayBySettingNumber(
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
                        message_for_edit,
                        state,
                        user_id,
                        setting_number,
                        is_test_generation,
                    ),
                ]
        else:
            stateData = await state.get_data()
            model_indexes_for_generation = stateData.get("model_indexes_for_generation", [])
            logger.info(f"Получен список моделей для индивидуальной генерации: {model_indexes_for_generation}")

            if setting_number == "all":
                result = await generateImagesByAllSettings(
                    message,
                    state,
                    user_id,
                    is_test_generation,
                    True,
                )
            else:
                # Инициализация переменной message_for_edit перед её использованием
                message_for_edit = await message.answer(
                    text.GET_PROMPT_SUCCESS_TEXT,
                )
                await message_for_edit.pin()
                result = await generateImages(
                    setting_number,
                    prompt,
                    message_for_edit,
                    state,
                    user_id,
                    is_test_generation,
                    with_randomizer,
                    model_indexes_for_generation
                )
                await message_for_edit.unpin()

        stateData = await state.get_data()

        if not result:
            raise Exception("Произошла ошибка при генерации изображения")

    except Exception as e:
        try:
            await message_for_edit.unpin()
        except Exception:
            pass
        logger.error(f"Ошибка при генерации изображения: {e}")
        traceback.print_exc()
        await message.answer(text.GENERATION_IMAGE_ERROR_TEXT)
        await state.clear()
        return
