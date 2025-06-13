from aiogram import types
from aiogram.fsm.context import FSMContext

from config import MOCK_MODE

from ..handlers.startGeneration.sendImageBlock import sendImageBlock
from .base64ToImage import base64ToImage
from .getReferenceImage import getReferenceImage
from utils.repository.istorage import ITaskStorage


async def process_image_block(job_id: str, model_name: str, setting_number: int, user_id: int, 
    state: FSMContext, message_id: int, is_test_generation: bool, checkOtherJobs: bool, task_repo: ITaskStorage,
    chat_id: int) -> bool:
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
        task_repo (ITaskStorage): репозиторий задач
        chat_id (int): id чата
    """
    data = await state.get_data()
    await task_repo.add_task(
        job_id=job_id,
        user_id=user_id,
        message_id=message_id,
        model_name=model_name,
        setting_number=setting_number,
        job_type=data.get("job_type"),
        is_test_generation=is_test_generation,
        check_other_jobs=checkOtherJobs,
        chat_id=data.get("chat_id"),
    )
    from ..jobs.check_job_status import check_job_status, CANCELLED_JOB_TEXT
    # Проверяем статус работы
    response_json = await check_job_status(
        job_id,
        setting_number,
        user_id,
        message_id,
        state,
        is_test_generation,
        checkOtherJobs,
        500,
    )

    # Если работа не завершена, то возвращаем False
    if not response_json or response_json == CANCELLED_JOB_TEXT:
        return False

    # Если работа завершена, то обрабатываем результаты
    try:
        if not MOCK_MODE:
            images_output = response_json.get("output", [])

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
