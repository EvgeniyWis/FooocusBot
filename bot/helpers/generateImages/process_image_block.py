from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.domain.entities.task import TaskImageBlockDTO
from bot.helpers.generateImages.getReferenceImage import getReferenceImage
from bot.helpers.jobs.check_job_status import (
    check_job_status,
)
from bot.helpers.jobs.constants import CANCELLED_JOB_TEXT
from bot.logger import logger
from bot.settings import settings
from bot.storage import get_redis_storage
from bot.utils import retryOperation
from bot.utils.images.base64_to_image import base64_to_image


async def process_image_block(
    job_id: str,
    model_name: str,
    group_number: int | str,
    user_id: int,
    state: FSMContext,
    message_id: int,
    is_test_generation: bool,
    checkOtherJobs: bool,
    chat_id: int,
) -> bool:
    """
    Функция для обработки работы по её id и после удачного завершения - отправки сообщения с изображениями

    Attributes:
        job_id (str): id работы
        model_name (str): название модели
        group_number (int): номер группы
        user_id (int): id пользователя
        state (FSMContext): контекст состояния
        message (types.Message): сообщение
        is_test_generation (bool): флаг, указывающий на тестовую генерацию
        checkOtherJobs (bool): флаг, указывающий на проверку других работ
        chat_id (int): id чата
    """

    if not settings.MOCK_IMAGES_MODE:
        redis_storage = get_redis_storage()
        task_dto = TaskImageBlockDTO(
            job_id=job_id,
            model_name=model_name,
            group_number=group_number,
            user_id=user_id,
            message_id=message_id,
            is_test_generation=is_test_generation,
            check_other_jobs=checkOtherJobs,
            chat_id=chat_id,
        )
        await redis_storage.add_task(
            settings.PROCESS_IMAGE_BLOCK_TASK,
            task_dto,
        )

        # Проверяем статус работы
        response_json = await retryOperation(
            check_job_status,
            5,
            2,
            job_id,
            group_number,
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
        if not settings.MOCK_IMAGES_MODE:
            images_output = response_json.get("output", [])

            if images_output == []:
                raise Exception(
                    "Не удалось сгенерировать изображения (ошибка обработки на RunPod)",
                )

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
        if not settings.MOCK_IMAGES_MODE:
            for i, image_data in enumerate(images_output):
                file_path = await base64_to_image(
                    image_data["base64"],
                    model_name,
                    i + 1,
                    user_id,
                    is_test_generation,
                )
                media_group.append(
                    types.InputMediaPhoto(
                        media=types.FSInputFile(file_path),
                    ),
                )

        # Если изображение первое в очереди, то отправляем его и инициализуем стейт (либо если это изображение, которое перегенерируется)
        state_data = await state.get_data()

        # Если изображение перегенерируется, то удаляем его из списка перегенерируемых изображений
        regenerated_models = state_data.get("regenerated_models", [])
        if model_name in regenerated_models:
            regenerated_models.remove(model_name)
            await state.update_data(
                regenerated_models=regenerated_models,
            )

        from helpers.handlers.startGeneration import sendImageBlock

        if not len(media_group):
            logger.error(
                f"Медиагруппа изображений для отправки пользователю {user_id} для модели {model_name} пуста: {media_group}",
            )
            return False

        await sendImageBlock(
            state,
            media_group,
            model_name,
            group_number,
            is_test_generation,
            user_id,
            generation_id=job_id,
        )

        return True

    except Exception as e:
        raise Exception(f"Ошибка при получении изображения: {e}")
