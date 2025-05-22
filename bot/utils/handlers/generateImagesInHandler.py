from utils.generateImages.generateImagesByAllSettings import generateImagesByAllSettings
from utils.generateImages.generateImageBlock import generateImageBlock
from aiogram import types
from aiogram.fsm.context import FSMContext
from utils import text
from utils.generateImages.dataArray.getDataArrayWithRootPrompt import getDataArrayWithRootPrompt
from logger import logger
import traceback
from utils.generateImages.generateImages import generateImages


# Функция для генерации изображения в зависимости от настроек
async def generateImagesInHandler(prompt: str, message: types.Message, state: FSMContext,
    user_id: int, is_test_generation: bool, setting_number: str, with_randomizer: bool = False):
    # Генерируем изображения
    try:
        if is_test_generation:
            if setting_number == "all":
                result = await generateImagesByAllSettings(message, state, user_id, is_test_generation)
            else:
                # Отправляем сообщение о получении промпта
                message_for_edit = await message.answer(
                    text.GET_PROMPT_SUCCESS_TEXT
                )
                # Прибавляем к каждому элементу массива корневой промпт
                dataArray = getDataArrayWithRootPrompt(int(setting_number), prompt)
                dataJSON = dataArray[0]["json"]
                model_name = dataArray[0]["model_name"]
                result = [await generateImageBlock(dataJSON, model_name, message_for_edit, state, user_id, setting_number, is_test_generation)]
        else:
            if setting_number == "all":
                result = await generateImagesByAllSettings(message, state, user_id, is_test_generation, True)
            else:
                message_for_edit = await message.answer(
                    text.GET_PROMPT_SUCCESS_TEXT
                )
                await message_for_edit.pin()
                result = await generateImages(int(setting_number), prompt, message_for_edit, state, user_id, is_test_generation, with_randomizer)
                await message_for_edit.unpin()
                
        stateData = await state.get_data()
        if result:
            if "stop_generation" not in stateData:
                await message.answer(text.GENERATE_IMAGE_SUCCESS_TEXT)
        else:
            if "stop_generation" not in stateData:
                raise Exception("Произошла ошибка при генерации изображения")

    except Exception as e:
        try:
            await message_for_edit.unpin()
        except:
            pass
        traceback.print_exc()
        await message.answer(text.GENERATION_IMAGE_ERROR_TEXT)
        await state.clear()
        logger.error(f"Произошла ошибка при генерации изображения: {e}")
        return