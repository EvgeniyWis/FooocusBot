from aiogram import types
from utils.generateImages.getReferenceImage import getReferenceImage
from utils import text
from utils.generateImages.base64ToImage import base64ToImage
from aiogram.fsm.context import FSMContext
from keyboards.user import keyboards
import shutil
import asyncio
from ..jobs.getJobID import getJobID
from ..jobs.checkJobStatus import checkJobStatus
from config import TEMP_FOLDER_PATH
from .upscaleImage import upscaleImage
from InstanceBot import bot
from logger import logger

# Функция для генерации изображений по объекту данных
async def generateImageBlock(dataJSON: dict, model_name: str, message: types.Message, state: FSMContext, 
    user_id: int, setting_number: str, is_test_generation: bool = False):
    # Получаем данные из стейта
    stateData = await state.get_data()
    stop_generation = stateData.get("stop_generation", False)

    if stop_generation:
        raise Exception("Генерация остановлена")

    # Делаем запрос на генерацию и получаем id работы
    job_id = await getJobID(dataJSON)

    # Проверяем статус работы
    response_json = await checkJobStatus(job_id, state, message, is_test_generation)

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

        # Обновляем сообщение о начале upscale
        stateData = await state.get_data()
        if "current_model_for_unique_prompt" in stateData:
            upscale_message = await message.edit_text(text.UPSCALE_IMAGES_PROGRESS_TEXT.format(model_name))

        # Создаем список задач для параллельного upscale
        upscale_tasks = [upscaleImage(image["base64"], dataJSON["input"]["negative_prompt"], dataJSON["input"]["base_model_name"]) for image in images_output]
        # Выполняем все задачи параллельно
        upscaled_images = await asyncio.gather(*upscale_tasks)

        # Обрабатываем результаты
        for i, upscale_image_data in enumerate(upscaled_images):
            base_64_data = await base64ToImage(upscale_image_data, model_name, i, user_id, is_test_generation)
            base_64_dataArray.append(base_64_data)
            media_group.append(types.InputMediaPhoto(media=types.FSInputFile(base_64_data)))
        
        # Удаляем сообщение про upscale
        if "current_model_for_unique_prompt" in stateData:
            try:
                await bot.delete_message(user_id, upscale_message.message_id)
            except Exception as e:
                logger.error(f"Ошибка при удалении сообщения про upscale: {e}")

        # Отправляем изображения
        message_with_media_group = await message.answer_media_group(media_group)

        if setting_number == "all":
            setting_number = stateData["current_setting_number_for_unique_prompt"]

        # Отправляем клавиатуру для выбора изображения
        await message.answer(text.SELECT_IMAGE_TEXT.format(model_name) if not is_test_generation else text.SELECT_TEST_IMAGE_TEXT.format(setting_number), 
        reply_markup=keyboards.selectImageKeyboard(model_name, setting_number) if not is_test_generation else keyboards.testGenerationImagesKeyboard(setting_number) if stateData["setting_number"] != "all" else None)

        # Сохраняем в стейт данные о медиагруппе, для её удаления
        await state.update_data(**{f"mediagroup_messages_ids_{model_name}": [i.message_id for i in message_with_media_group]})
        
        # Если это тестовая генерация, то удаляем изображения из папки temp/test/ и сами папки
        if is_test_generation:
            shutil.rmtree(f"{TEMP_FOLDER_PATH}/test_{user_id}")
            return
        
        return True
        
    except Exception as e:
        raise Exception(f"Ошибка при получении изображения: {e}")
