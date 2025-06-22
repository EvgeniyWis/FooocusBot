from adapters.redis_task_storage_repository import key_for_image
from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.assets.mocks.links import MOCK_FACEFUSION_PATH
from bot.domain.entities.task import TaskProcessImageDTO
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
from bot.storage import get_redis_storage


async def process_image(
    call: types.CallbackQuery,
    state: FSMContext,
    model_name: str,
    image_index: int,
) -> bool:
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

    result_path = None

    process_image_step = await get_current_process_image_step(
        state,
        model_name,
    )

    if not settings.MOCK_MODE:
        if (
            settings.UPSCALE_MODE
            and process_image_step == ProcessImageStep.UPSCALE
        ):
            logger.info("Запускаем upscale")
            await process_upscale_image(call, state, image_index, model_name)

            process_image_step = await update_process_image_step(
                state,
                model_name,
                ProcessImageStep.FACEFUSION,
            )

        if (
            settings.FACEFUSION_MODE
            and process_image_step == ProcessImageStep.FACEFUSION
        ):
            logger.info("Запускаем faceswap")
            result_path = await process_faceswap_image(
                call,
                state,
                image_index,
                model_name,
            )

            if result_path:
                await state.update_data(
                    {f"{model_name}_result_path": result_path},
                )
                process_image_step = await update_process_image_step(
                    state,
                    model_name,
                    ProcessImageStep.SAVE,
                )
            else:
                logger.warning(
                    "Faceswap не вернул result_path — не двигаем шаг",
                )
                return False

        if process_image_step == ProcessImageStep.SAVE:
            logger.info(
                "Этап SAVE — восстанавливаем result_path из state",
            )
            state_data = await state.get_data()
            result_path = state_data.get(f"{model_name}_result_path")

            if not result_path:
                logger.warning(
                    "result_path пустой при SAVE — откат к FACEFUSION",
                )
                await update_process_image_step(
                    state,
                    model_name,
                    ProcessImageStep.FACEFUSION,
                )
                return await process_image(
                    call,
                    state,
                    model_name,
                    image_index,
                )

    else:
        result_path = MOCK_FACEFUSION_PATH

    if not result_path:
        logger.warning("result_path пустой — завершаем")
        return False

    logger.info(f"Результат обработки: {result_path}")

    if process_image_step == ProcessImageStep.SAVE:
        logger.info("Сохраняем изображение")
        await process_save_image(call, state, model_name, result_path)

    redis_storage = get_redis_storage()
    await redis_storage.delete_task(
        settings.PROCESS_IMAGE_TASK,
        key_for_image(call.from_user.id, image_index, model_name),
    )

    return True
