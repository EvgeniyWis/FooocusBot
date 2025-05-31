from utils.generateImages.dataArray.getDataByModelName import getDataByModelName
from utils.generateImages.generateImagesByAllSettings import generateImagesByAllSettings
from utils.generateImages.generateImageBlock import generateImageBlock
from aiogram import types
from aiogram.fsm.context import FSMContext
from utils import text
from utils.generateImages.dataArray.getDataArrayWithRootPrompt import getDataArrayWithRootPrompt
from logger import logger
import traceback
from utils.generateImages.generateImages import generateImages
from utils.generateImages.dataArray.getModelNameIndex import getModelNameIndex
import asyncio
from utils.generateImages.dataArray.getSettingNumberByModelName import getSettingNumberByModelName


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
            stateData = await state.get_data()
            model_names_for_generation = stateData.get("model_names_for_generation", [])
            logger.info(f"Получен список моделей для индивидуальной генерации: {model_names_for_generation}")

            if len(model_names_for_generation) > 0:
                for model_name in model_names_for_generation:
                    logger.info(f"Генерируем изображения для индивидуальной модели: {model_name}")

                    # Получаем порядковый номер модели
                    model_name_index = getModelNameIndex(model_name)

                    # Отправляем сообщение о генерации изображений по имени модели
                    await message.answer(text.GENERATE_IMAGES_BY_MODEL_NAME_TEXT.format(model_name, model_name_index))

                    # Получаем данные о модели
                    dataArray = await getDataByModelName(model_name)

                    # Прибавляем корневой промпт
                    dataArray["json"]['input']['prompt'] += " " + prompt
                    dataJSON = dataArray["json"]

                    # Получаем номер настройки по названию модели
                    setting_number = getSettingNumberByModelName(model_name)

                    # Запускаем задачу для генерации изображений
                    asyncio.create_task(generateImageBlock(dataJSON, model_name, message, state, user_id, setting_number, is_test_generation))
                return
            
            elif setting_number == "all":
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
            if not stateData["stop_generation"]:
                await message.answer(text.GENERATE_IMAGE_SUCCESS_TEXT)
        else:
            if not stateData["stop_generation"]:
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