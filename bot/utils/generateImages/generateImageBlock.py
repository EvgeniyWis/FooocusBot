from aiogram import types
from utils.generateImages.getReferenceImage import getReferenceImage
from utils import text
from utils.generateImages.base64ToImage import base64ToImage
from aiogram.fsm.context import FSMContext
from keyboards import start_generation_keyboards
import shutil
from ..jobs.getJobID import getJobID
from ..jobs.checkJobStatus import checkJobStatus
from config import TEMP_FOLDER_PATH
from utils.generateImages.dataArray.getModelNameIndex import getModelNameIndex


# Функция для генерации изображений по объекту данных
async def generateImageBlock(dataJSON: dict, model_name: str, message: types.Message, state: FSMContext, 
    user_id: int, setting_number: str, is_test_generation: bool = False, checkOtherJobs: bool = True):
    # Получаем данные из стейта
    stateData = await state.get_data()
    stop_generation = stateData.get("stop_generation", False)

    if stop_generation:
        try:
            message.unpin()
        except:
            pass
        raise Exception("Генерация остановлена")

    # Делаем запрос на генерацию и получаем id работы
    job_id = await getJobID(dataJSON)

    # Проверяем статус работы
    response_json = await checkJobStatus(job_id, state, message, is_test_generation, checkOtherJobs)

    try:
        images_output = response_json["output"]
        
        if images_output == []:
            raise Exception("Не удалось сгенерировать изображения")

        media_group = []
        base_64_dataArray = []

        # Получаем референсное изображение и добавляем его в медиагруппу
        reference_image = await getReferenceImage(model_name)
        if reference_image:
            media_group.append(types.InputMediaPhoto(media=types.FSInputFile(reference_image)))

        # Обрабатываем результаты
        for i, image_data in enumerate(images_output):
            base_64_data = await base64ToImage(image_data["base64"], model_name, i, user_id, is_test_generation)
            base_64_dataArray.append(base_64_data)
            media_group.append(types.InputMediaPhoto(media=types.FSInputFile(base_64_data)))

        # Отправляем изображения
        message_with_media_group = await message.answer_media_group(media_group)

        if setting_number == "all":
            setting_number = stateData["current_setting_number_for_unique_prompt"]

        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

        # Отправляем клавиатуру для выбора изображения
        await message.answer(text.SELECT_IMAGE_TEXT.format(model_name, model_name_index) if not is_test_generation else text.SELECT_TEST_IMAGE_TEXT.format(setting_number), 
        reply_markup=start_generation_keyboards.selectImageKeyboard(model_name, setting_number) if not is_test_generation else start_generation_keyboards.testGenerationImagesKeyboard(setting_number) if stateData["setting_number"] != "all" else None)

        # Сохраняем в стейт данные о медиагруппе, для её удаления
        await state.update_data(**{f"mediagroup_messages_ids_{model_name}": [i.message_id for i in message_with_media_group]})
        
        # Если это тестовая генерация, то удаляем изображения из папки temp/test/ и сами папки
        if is_test_generation:
            shutil.rmtree(f"{TEMP_FOLDER_PATH}/test_{user_id}")
            return
        
        return True
        
    except Exception as e:
        raise Exception(f"Ошибка при получении изображения: {e}")
