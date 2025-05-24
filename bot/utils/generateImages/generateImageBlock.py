from aiogram import types
from .getReferenceImage import getReferenceImage
from .base64ToImage import base64ToImage
from aiogram.fsm.context import FSMContext
from ..jobs.getJobID import getJobID
from ..jobs.checkJobStatus import checkJobStatus
from ..handlers.sendImageBlock import sendImageBlock

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

        # Если изображение первое в очереди, то отправляем его и инициализуем стейт
        stateData = await state.get_data()
        if "media_groups_for_generation" not in stateData:
            await state.update_data(media_groups_for_generation=[])

            # Отправляем изображение
            await sendImageBlock(message, state, media_group, model_name, setting_number, is_test_generation)
            
        else: # Если изображение не первое в очереди, то добавляем его в стейт и оно отправится только после подтверждения генерации у прошлого изображения
            dataForUpdate = {f"{model_name}": media_group}
            media_groups_for_generation = stateData["media_groups_for_generation"]
            media_groups_for_generation.append(dataForUpdate)
            await state.update_data(media_groups_for_generation=media_groups_for_generation)
        
        return True
        
    except Exception as e:
        raise Exception(f"Ошибка при получении изображения: {e}")
