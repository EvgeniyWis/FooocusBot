import shutil
import logging

from aiogram import types
from aiogram.fsm.context import FSMContext
from config import MOCK_MODE, TEMP_FOLDER_PATH
from keyboards import start_generation_keyboards

from ... import text
from ...generateImages.dataArray import getDataByModelName, getModelNameIndex


# Функция для отправки сообщения со сгенерируемыми изображениями
async def sendImageBlock(message: types.Message, state: FSMContext, media_group: list, model_name: str,
    setting_number: str, is_test_generation: bool, user_id: int):
    try:
        # Отправляем изображения
        await message.answer_media_group(media_group)
    except Exception as e:
        logging.error(f"Ошибка при отправке медиагруппы: {e}")
        try:
            await message.answer("Произошла ошибка при отправке изображений, но продолжаем работу...")
        except:
            pass

    try:
        # Получаем данные из стейта
        stateData = await state.get_data()

        # Если номер настройки все, то получаем номер настройки из стейта
        if setting_number == "all":
            setting_number = stateData.get("current_setting_number_for_unique_prompt", 1)

        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

        # Получаем данные модели
        model_data = await getDataByModelName(model_name)

        # Отправляем клавиатуру для выбора изображения
        try:
            await message.answer(text.SELECT_IMAGE_TEXT.format(model_name, model_name_index) if not is_test_generation else text.SELECT_TEST_IMAGE_TEXT.format(setting_number),
            reply_markup=start_generation_keyboards.selectImageKeyboard(model_name, setting_number, model_data["json"]["input"]["image_number"])
            if not is_test_generation else start_generation_keyboards.testGenerationImagesKeyboard(setting_number) if stateData.get("setting_number", 1) != "all" else None)
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения с клавиатурой: {e}")
            try:
                await message.answer("Произошла ошибка при отправке клавиатуры...")
            except:
                pass

        # Если это тестовая генерация, то удаляем изображения из папки temp/test/ и сами папки
        if is_test_generation and not MOCK_MODE:
            try:
                shutil.rmtree(f"{TEMP_FOLDER_PATH}/test_{user_id}")
            except Exception as e:
                logging.error(f"Ошибка при удалении временных файлов: {e}")
    except Exception as e:
        logging.error(f"Критическая ошибка в функции sendImageBlock: {e}")
        try:
            await message.answer("Произошла ошибка, но бот продолжает работу...")
        except:
            pass
