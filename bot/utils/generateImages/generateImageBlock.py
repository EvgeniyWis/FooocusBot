from aiogram import types
from aiogram.fsm.context import FSMContext
from config import MOCK_MODE

from ..handlers.startGeneration.sendImageBlock import sendImageBlock
from ..jobs.checkJobStatus import checkJobStatus
from ..jobs.getJobID import getJobID
from .base64ToImage import base64ToImage
from .getReferenceImage import getReferenceImage
from .dataArray.getSettingNumberByModelName import getSettingNumberByModelName


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
    stop_generation = stateData.get("stop_generation", False)

    if stop_generation:
        try:
            message.unpin()
        except:
            pass
        raise Exception("Генерация остановлена")

    if not MOCK_MODE:
        # Получаем номер настройки по имени модели
        setting_number = getSettingNumberByModelName(model_name)

        # Делаем запрос на генерацию и получаем id работы
        job_id = await getJobID(dataJSON, setting_number)

        # Проверяем статус работы
        response_json = await checkJobStatus(
            job_id,
            setting_number,
            state,
            message,
            is_test_generation,
            checkOtherJobs,
        )

    try:
        if not MOCK_MODE:
            images_output = response_json["output"]

            if images_output == []:
                raise Exception("Не удалось сгенерировать изображения")

        media_group = []
        base_64_dataArray = []

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
                base_64_data = await base64ToImage(
                    image_data["base64"],
                    model_name,
                    i,
                    user_id,
                    is_test_generation,
                )
                base_64_dataArray.append(base_64_data)
                media_group.append(
                    types.InputMediaPhoto(
                        media=types.FSInputFile(base_64_data),
                    ),
                )

        # Если изображение первое в очереди, то отправляем его и инициализуем стейт (либо если это изображение, которое перегенерируется)
        stateData = await state.get_data()
        if (
            stateData["media_groups_for_generation"] == None
            or model_name in stateData["regenerate_images"]
        ):
            # Обновляем стейт
            if stateData["media_groups_for_generation"] == None:
                await state.update_data(media_groups_for_generation=[])

            # Если изображение перегенерируется, то удаляем его из списка перегенерируемых изображений
            elif model_name in stateData["regenerate_images"]:
                stateData["regenerate_images"].remove(model_name)
                await state.update_data(
                    regenerate_images=stateData["regenerate_images"],
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

        else:  # Если изображение не первое в очереди, то добавляем его в стейт и оно отправится только после подтверждения генерации у прошлого изображения
            dataForUpdate = {f"{model_name}": media_group}
            stateData["media_groups_for_generation"].append(dataForUpdate)
            await state.update_data(
                media_groups_for_generation=stateData[
                    "media_groups_for_generation"
                ],
            )

        return True

    except Exception as e:
        raise Exception(f"Ошибка при получении изображения: {e}")
