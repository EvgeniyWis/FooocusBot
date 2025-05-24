from aiogram import types
from utils import text
from aiogram.fsm.context import FSMContext
from keyboards import start_generation_keyboards
import shutil
from config import TEMP_FOLDER_PATH
from utils.generateImages.dataArray.getModelNameIndex import getModelNameIndex
from utils.generateImages.dataArray.getDataByModelName import getDataByModelName


# Функция для отправки сообщения со сгенерируемыми изображениями
async def sendImageBlock(message: types.Message, state: FSMContext, media_group: list, model_name: str, 
    setting_number: str, is_test_generation: bool):
    # Получаем id пользователя
    user_id = message.from_user.id
    
    # Отправляем изображения
    message_with_media_group = await message.answer_media_group(media_group)

    # Получаем данные из стейта
    stateData = await state.get_data()

    # Если номер настройки все, то получаем номер настройки из стейта
    if setting_number == "all":
        setting_number = stateData["current_setting_number_for_unique_prompt"]

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Получаем данные модели
    model_data = await getDataByModelName(model_name)

    # Отправляем клавиатуру для выбора изображения
    await message.answer(text.SELECT_IMAGE_TEXT.format(model_name, model_name_index) if not is_test_generation else text.SELECT_TEST_IMAGE_TEXT.format(setting_number), 
    reply_markup=start_generation_keyboards.selectImageKeyboard(model_name, setting_number, model_data["json"]["input"]["image_number"]) 
    if not is_test_generation else start_generation_keyboards.testGenerationImagesKeyboard(setting_number) if stateData["setting_number"] != "all" else None)

    # Сохраняем в стейт данные о медиагруппе, для её удаления
    await state.update_data(**{f"mediagroup_messages_ids_{model_name}": [i.message_id for i in message_with_media_group]})
    
    # Если это тестовая генерация, то удаляем изображения из папки temp/test/ и сами папки
    if is_test_generation:
        shutil.rmtree(f"{TEMP_FOLDER_PATH}/test_{user_id}")
        return