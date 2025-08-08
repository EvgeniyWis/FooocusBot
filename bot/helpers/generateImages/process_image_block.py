from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.domain.entities.task import TaskImageBlockDTO
from bot.helpers.generateImages.dataArray import (
    get_group_number_by_model_name,
    get_setting_number_by_model_name,
)
from bot.helpers.generateImages.getReferenceImage import getReferenceImage
from bot.helpers.jobs.check_job_status import (
    check_job_status,
)
from bot.helpers.jobs.constants import CANCELLED_JOB_TEXT
from bot.app.core.logging import logger
from bot.app.config.settings import settings
from bot.storage import get_redis_storage
from bot.utils import retryOperation
from bot.utils.images.base64_to_image import base64_to_image


async def process_image_block(
    job_id: str,
    model_name: str,
    user_id: int,
    state: FSMContext,
    message_id: int,
    checkOtherJobs: bool,
    chat_id: int,
    model_key: str = None,
) -> bool:
    """
    Функция для обработки работы по её id и после удачного завершения - отправки сообщения с изображениями

    Attributes:
        job_id (str): id работы
        model_name (str): название модели
        user_id (int): id пользователя
        state (FSMContext): контекст состояния
        message (types.Message): сообщение
        checkOtherJobs (bool): флаг, указывающий на проверку других работ
        chat_id (int): id чата
    """

    # Получаем номер настройки по имени модели
    setting_number = get_setting_number_by_model_name(model_name)

    # Получаем номер группы по имени модели
    group_number = get_group_number_by_model_name(model_name)

    if not settings.MOCK_IMAGES_MODE:
        redis_storage = get_redis_storage()
        task_dto = TaskImageBlockDTO(
            job_id=job_id,
            model_name=model_name,
            setting_number=setting_number,
            user_id=user_id,
            message_id=message_id,
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
            setting_number,
            group_number,
            user_id,
            message_id,
            state,
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
                    job_id,
                    i + 1,
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
            user_id,
            job_id=job_id,
            model_key=model_key,
        )

        return True

    except Exception as e:
        raise Exception(f"Ошибка при получении изображения: {e}")
