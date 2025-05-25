from ...generateImages.dataArray import getDataByModelName, getDataArrayWithRootPrompt, getModelNameIndex
from ...generateImages import generateImagesByAllSettings, generateImageBlock, generateImages
from ... import text
from aiogram import types
from aiogram.fsm.context import FSMContext
from logger import logger
import traceback
import asyncio
from keyboards import start_generation_keyboards


# Функция для генерации изображения в зависимости от настроек
async def generateImagesInHandler(prompt: str, message: types.Message, state: FSMContext,
    user_id: int, is_test_generation: bool, setting_number: str, with_randomizer: bool = False):
    # Инициализируем стейт
    await state.update_data(models_for_generation_queue=[])
    await state.update_data(regenerate_images=[])
    await state.update_data(will_be_sent_generated_images_count=0)
    await state.update_data(finally_sent_generated_images_count=0)
    await state.update_data(total_images_count=0)
    await state.update_data(saved_images_count=0)
    await state.update_data(saved_videos_count=0)
    await state.update_data(media_groups_for_generation=None)
    await state.update_data(generation_step=1)

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

            if "model_name_for_generation" in stateData:
                model_name = stateData["model_name_for_generation"]

                # Получаем порядковый номер модели
                model_name_index = getModelNameIndex(model_name)

                # Отправляем сообщение о генерации изображений по имени модели
                await message.answer(text.GENERATE_IMAGES_BY_MODEL_NAME_TEXT.format(model_name, model_name_index))

                # Получаем данные о модели
                dataArray = await getDataByModelName(model_name)
                dataJSON = dataArray["json"]

                # Генерируем изображения
                await generateImageBlock(dataJSON, model_name, message, state, user_id, setting_number, is_test_generation)
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

        if not is_test_generation:
            if result:
                if "stop_generation" not in stateData:
                    finally_sent_generated_images_count = stateData["finally_sent_generated_images_count"]
                total_images_count = stateData["total_images_count"]
                
                # Ждём когда список моделей для генерации станет пустым
                while finally_sent_generated_images_count < total_images_count:
                    stateData = await state.get_data()
                    finally_sent_generated_images_count = stateData["finally_sent_generated_images_count"]
                    total_images_count = stateData["total_images_count"]
                    await asyncio.sleep(10)

                # Очищаем список медиагрупп
                await state.update_data(media_groups_for_generation=None)

                # И только после этого отправляем сообщение о успешной генерации с возможностью начать этап сохранения изображений
                await message.answer(text.GENERATE_IMAGES_SUCCESS_TEXT, 
                reply_markup=start_generation_keyboards.saveImagesKeyboard())

                # Ставим, что начался 2 этап
                await state.update_data(generation_step=2)
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