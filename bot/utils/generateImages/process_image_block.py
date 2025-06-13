from aiogram import types
from aiogram.fsm.context import FSMContext

from config import MOCK_MODE

from ..handlers.startGeneration.sendImageBlock import sendImageBlock
from ..jobs.checkJobStatus import checkJobStatus
from .base64ToImage import base64ToImage
from .getReferenceImage import getReferenceImage
from RunBot import redis_task_storage


async def process_image_block(job_id: str, model_name: str, setting_number: int, user_id: int, 
    state: FSMContext, message_id: int, is_test_generation: bool, checkOtherJobs: bool) -> bool:
    """
    Функция для обработки работы по её id и после удачного завершения - отправки сообщения с изображениями
    
    Attributes:
        job_id (str): id работы
        model_name (str): название модели
        setting_number (int): номер настройки
        user_id (int): id пользователя
        state (FSMContext): контекст состояния
        message (types.Message): сообщение
        is_test_generation (bool): флаг, указывающий на тестовую генерацию
        checkOtherJobs (bool): флаг, указывающий на проверку других работ
    """
    data = await state.get_data()
    await redis_task_storage.add_task(
        job_id=job_id,
        model_name=model_name,
        setting_number=setting_number,
        user_id=user_id,
        message_id=message_id,
        is_test_generation=is_test_generation,
        check_other_jobs=checkOtherJobs,
        job_type=data.get("job_type"),
    )
    # Проверяем статус работы
    response_json = await checkJobStatus(
        job_id,
        setting_number,
        user_id,
        message_id,
        state,
        is_test_generation,
        checkOtherJobs,
        500
    )

    # Если работа не завершена, то возвращаем False
    if not response_json:
        return False

    # Если работа завершена, то обрабатываем результаты
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
        regenerated_models = stateData.get("regenerated_models", [])
        if model_name in regenerated_models:
            regenerated_models.remove(model_name)
            await state.update_data(
                regenerated_models=regenerated_models,
            )

        # Отправляем изображение
        await sendImageBlock(
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
