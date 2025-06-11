from aiogram import types
from aiogram.fsm.context import FSMContext
from config import MOCK_MODE

from ..handlers.startGeneration.sendImageBlock import sendImageBlock
from ..jobs.checkJobStatus import checkJobStatus
from ..jobs.getJobID import getJobID
from .base64ToImage import base64ToImage
from .getReferenceImage import getReferenceImage
from .dataArray.getSettingNumberByModelName import getSettingNumberByModelName
from logger import logger


# Функция для генерации изображений по объекту данных
async def generateImageBlock(
    dataJSON: dict,
    model_name: str,
    message: types.Message,
    state: FSMContext,
    user_id: int,
    setting_number: str,
    is_test_generation: bool = False,
    checkOtherJobs: bool = True,
):
    # Получаем данные из стейта
    stateData = await state.get_data()

    if not MOCK_MODE:
        # Получаем номер настройки по имени модели
        setting_number = getSettingNumberByModelName(model_name)

        # Логируем наш json
        logger.info(f"Отправляем запрос на генерацию изображений с данными: {dataJSON}")

        # Делаем запрос на генерацию и получаем id работы
        job_id = await getJobID(dataJSON, setting_number, state)

        # Проверяем статус работы
        response_json = await checkJobStatus(
            job_id,
            setting_number,
            state,
            message,
            is_test_generation,
            checkOtherJobs,
            500
        )

        if not response_json:
            return False

    try:
        if not MOCK_MODE:
            images_output = response_json["output"]

            if images_output == []:
                raise Exception("Не удалось сгенерировать изображения")

        media_group = []

        # Получаем референсное изображение и добавляем его в медиагруппу
        reference_image = await getReferenceImage(model_name)
        if reference_image:
            media_group.append(
                types.InputMediaPhoto(
                    media=types.FSInputFile(reference_image),
                ),
            )

        # Обрабатываем результаты
        if not MOCK_MODE:
            for i, image_data in enumerate(images_output):
                file_path = await base64ToImage(
                    image_data["base64"],
                    model_name,
                    i,
                    user_id,
                    is_test_generation,
                )
                media_group.append(
                    types.InputMediaPhoto(
                        media=types.FSInputFile(file_path),
                    ),
                )

        # Если изображение первое в очереди, то отправляем его и инициализуем стейт (либо если это изображение, которое перегенерируется)
        stateData = await state.get_data()
        
        # Если изображение перегенерируется, то удаляем его из списка перегенерируемых изображений
        regenerate_images = stateData.get("regenerate_images", [])
        if model_name in regenerate_images:
            regenerate_images.remove(model_name)
            await state.update_data(
                regenerate_images=regenerate_images,
            )

        # Отправляем изображение
        await sendImageBlock(
            message,
            state,
            media_group,
            model_name,
            setting_number,
            is_test_generation,
            user_id,
        )

        return True

    except Exception as e:
        raise Exception(f"Ошибка при получении изображения: {e}")
