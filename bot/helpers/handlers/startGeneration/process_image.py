from adapters.redis_task_storage_repository import key_for_image
from aiogram import types
from aiogram.fsm.context import FSMContext
from domain.entities.task import TaskProcessImageDTO
from storage import get_redis_storage

from bot.assets.mocks.links import (
    MOCK_FACEFUSION_PATH,
)
from bot.helpers.handlers.startGeneration.image_processes import (
    ProcessImageStep,
    get_current_process_image_step,
    process_faceswap_image,
    process_save_image,
    process_upscale_image,
    update_process_image_step,
)
from bot.logger import logger
from bot.settings import settings


async def process_image(
    call: types.CallbackQuery,
    state: FSMContext,
    model_name: str,
    image_index: int,
):
    """
    Обрабатывает изображение после выбора индекса среди сгенерированных изображений.
    Последовательно производит над выбранным изображением операции upscale, faceswap
    и сохраняет результат на Google Drive.
    В стейте сохраняется каfждый текущий шаг обработки изображения для его возобновления в случае ошибки.

    Attributes:
        - call: types.CallbackQuery, объект вызова
        - model_name: str, название модели
        - image_index: int, индекс выбранного изображения

    Returns:
        - bool, True если изображение успешно обработано, False если нет
    """

    redis_storage = get_redis_storage()
    task_dto = TaskProcessImageDTO(
        user_id=call.from_user.id,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        callback_data=call.data,
        model_name=model_name,
        image_index=image_index,
    )
    await redis_storage.add_task(settings.PROCESS_IMAGE_TASK, task_dto)

    # Инициализируем результирующий путь
    result_path = None

    # Получаем текущий этап обработки изображения для модели
    process_image_step = await get_current_process_image_step(
        state,
        model_name,
    )

    # Если не в режиме мока, то продолжаем генерацию
    if not settings.MOCK_MODE:
        # Меняем текст на сообщении о начале upscale
        if (
            settings.UPSCALE_MODE
            and process_image_step == ProcessImageStep.UPSCALE
        ):
            await process_upscale_image(
                call,
                state,
                image_index,
                model_name,
            )

            # Меняем шаг обработки изображения на faceswap
            process_image_step = await update_process_image_step(
                state,
                model_name,
                ProcessImageStep.FACEFUSION,
            )

        if settings.FACEFUSION_MODE:
            if process_image_step == ProcessImageStep.FACEFUSION:
                result_path = await process_faceswap_image(
                    call,
                    state,
                    image_index,
                    model_name,
                )

                # Меняем шаг обработки изображения на save
                process_image_step = await update_process_image_step(
                    state,
                    model_name,
                    ProcessImageStep.SAVE,
                )

        else:
            result_path = MOCK_FACEFUSION_PATH

    else:
        result_path = MOCK_FACEFUSION_PATH

    # Если результат замены лица не найден, то завершаем генерацию и уменьшаем кол-во ожидаемых изображений
    if not result_path:
        return False

    logger.info(f"Результат замены лица: {result_path}")

    # Сохраняем изображение
    if process_image_step == ProcessImageStep.SAVE:
        await process_save_image(call, state, model_name, result_path)

    redis_storage = get_redis_storage()
    await redis_storage.delete_task(
        settings.PROCESS_IMAGE_TASK,
        key_for_image(call.from_user.id, image_index, model_name),
    )

    return True
