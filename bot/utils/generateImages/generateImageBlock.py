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

# Функция для генерации изображений по объекту данных
async def generateImageBlock(dataJSON: dict, model_name: str, message: types.Message, state: FSMContext, 
    user_id: int, setting_number: str, is_test_generation: bool = False):
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
        media_group.append(types.InputMediaPhoto(media=types.FSInputFile(reference_image)))

        # Обновляем сообщение о начале upscale
        stateData = await state.get_data()
        if "jobs" in stateData:
            await message.edit_text(text.UPSCALE_IMAGES_PROGRESS_TEXT.format(model_name))

        # Создаем список задач для параллельного upscale
        upscale_tasks = [upscaleImage(image["base64"]) for image in images_output]
        # Выполняем все задачи параллельно
        upscaled_images = await asyncio.gather(*upscale_tasks)

        # Обрабатываем результаты
        for i, upscale_image_data in enumerate(upscaled_images):
            base_64_data = await base64ToImage(upscale_image_data, model_name, i, user_id, is_test_generation)
            base_64_dataArray.append(base_64_data)
            media_group.append(types.InputMediaPhoto(media=types.FSInputFile(base_64_data)))
        
        # Удаляем сообщение про upscale
        if "jobs" in stateData:
            await bot.delete_message(user_id, message.message_id)

        # Отправляем изображения
        message_with_media_group = await message.answer_media_group(media_group)
        
        # Отправляем клавиатуру для выбора изображения
        await message.answer(text.SELECT_IMAGE_TEXT.format(model_name) if not is_test_generation else text.SELECT_TEST_IMAGE_TEXT.format(setting_number), 
        reply_markup=keyboards.selectImageKeyboard(model_name) if not is_test_generation else None)

        # Сохраняем в стейт данные о медиагруппе, для её удаления
        await state.update_data(**{f"mediagroup_messages_ids_{model_name}": [i.message_id for i in message_with_media_group]})
        
        # Если это тестовая генерация, то удаляем изображения из папки temp/test/ и сами папки
        if is_test_generation:
            shutil.rmtree(f"{TEMP_FOLDER_PATH}/test_{user_id}")
            return
        
        return True
        
    except Exception as e:
        raise Exception(f"Ошибка при получении изображения: {e}")
