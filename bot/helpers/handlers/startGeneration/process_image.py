import os

from adapters.redis_task_storage_repository import key_for_image
from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.assets.mocks.links import MOCK_FACEFUSION_PATH
from bot.constants import TEMP_FOLDER_PATH
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
):
    """
    Обрабатывает изображение после выбора индекса среди сгенерированных изображений.
    Последовательно производит над выбранным изображением операции upscale, faceswap
    и сохраняет результат на Google Drive.
    В стейте сохраняется каfждый текущий шаг обработки изображения для его возобновления в случае ошибки.

    Attributes:
        - call: types.CallbackQuery, объект вызова
        - state: FSMContext, стейт
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

    result_path = None

    logger.info(
        f"[process_image] model_name={model_name}, image_index={image_index}, call.from_user.id={call.from_user.id}",
    )

    process_image_step = await get_current_process_image_step(
        state,
        model_name,
        image_index,
    )
    logger.info(
        f"[process_image] step for ({model_name}, {image_index}) = {process_image_step}",
    )

    if not settings.MOCK_IMAGES_MODE:
        temp_image_path = (
            TEMP_FOLDER_PATH
            / f"{model_name}_{call.from_user.id}"
            / f"{image_index}.jpg"
        )
        if (
            settings.UPSCALE_MODE
            and process_image_step == ProcessImageStep.UPSCALE
        ):
            logger.info(
                f"[process_image] UPSCALE START: model_name={model_name}, image_index={image_index}, user_id={call.from_user.id}",
            )
            logger.info(
                f"[process_image] temp dir before UPSCALE: {os.listdir(TEMP_FOLDER_PATH / f'{model_name}_{call.from_user.id}') if (TEMP_FOLDER_PATH / f'{model_name}_{call.from_user.id}').exists() else 'NO_DIR'}",
            )
            logger.info(f"Запускаем upscale для ({model_name}, {image_index})")
            await process_upscale_image(call, state, image_index, model_name)
            logger.info(
                f"[process_image] UPSCALE END: model_name={model_name}, image_index={image_index}, user_id={call.from_user.id}, file exists={os.path.exists(temp_image_path)}",
            )
            logger.info(
                f"[process_image] temp dir after UPSCALE: {os.listdir(TEMP_FOLDER_PATH / f'{model_name}_{call.from_user.id}') if (TEMP_FOLDER_PATH / f'{model_name}_{call.from_user.id}').exists() else 'NO_DIR'}",
            )
            process_image_step = await update_process_image_step(
                state,
                model_name,
                image_index,
                ProcessImageStep.FACEFUSION,
            )
            logger.info(
                f"[process_image] step updated to FACEFUSION for ({model_name}, {image_index})",
            )

        if (
            settings.FACEFUSION_MODE
            and process_image_step == ProcessImageStep.FACEFUSION
        ):
            logger.info(
                f"[process_image] FACEFUSION START: model_name={model_name}, image_index={image_index}, user_id={call.from_user.id}",
            )
            faceswap_target_path = temp_image_path
            logger.info(
                f"[process_image] Проверка файла перед faceswap: {faceswap_target_path} exists={os.path.exists(faceswap_target_path)}",
            )
            logger.info(
                f"[process_image] temp dir before FACEFUSION: {os.listdir(TEMP_FOLDER_PATH / f'{model_name}_{call.from_user.id}') if (TEMP_FOLDER_PATH / f'{model_name}_{call.from_user.id}').exists() else 'NO_DIR'}",
            )
            if not os.path.exists(faceswap_target_path):
                logger.warning(
                    f"[process_image] Файл не найден для faceswap: {faceswap_target_path}",
                )
                return False
            result_path = await process_faceswap_image(
                call,
                state,
                image_index,
                model_name,
            )
            logger.info(
                f"[process_image] FACEFUSION END: model_name={model_name}, image_index={image_index}, user_id={call.from_user.id}, file exists={os.path.exists(faceswap_target_path)}",
            )
            logger.info(
                f"[process_image] temp dir after FACEFUSION: {os.listdir(TEMP_FOLDER_PATH / f'{model_name}_{call.from_user.id}') if (TEMP_FOLDER_PATH / f'{model_name}_{call.from_user.id}').exists() else 'NO_DIR'}",
            )
            if result_path:
                await state.update_data(
                    {f"{model_name}_{image_index}_result_path": result_path},
                )
                process_image_step = await update_process_image_step(
                    state,
                    model_name,
                    image_index,
                    ProcessImageStep.SAVE,
                )
                logger.info(
                    f"[process_image] step updated to SAVE for ({model_name}, {image_index})",
                )
            else:
                logger.warning(
                    f"Faceswap не вернул result_path для ({model_name}, {image_index}) — не двигаем шаг",
                )
                return False

        if process_image_step == ProcessImageStep.SAVE:
            logger.info(
                f"Этап SAVE — восстанавливаем result_path из state для ({model_name}, {image_index})",
            )
            state_data = await state.get_data()
            result_path = state_data.get(
                f"{model_name}_{image_index}_result_path",
            )
            logger.info(
                f"[process_image] result_path для ({model_name}, {image_index}) = {result_path}",
            )

            if not result_path:
                logger.warning(
                    f"result_path пустой при SAVE для ({model_name}, {image_index}) — откат к FACEFUSION",
                )
                await update_process_image_step(
                    state,
                    model_name,
                    image_index,
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

    if (
        process_image_step == ProcessImageStep.SAVE
        or not settings.FACEFUSION_MODE
    ):
        logger.info(f"Сохраняем изображение для ({model_name}, {image_index})")
        await process_save_image(
            call,
            state,
            model_name,
            result_path,
            image_index,
        )

        state_data = await state.get_data()
        process_images_steps = state_data.get("process_images_steps", [])
        process_images_steps = [
            item
            for item in process_images_steps
            if not (
                item["model_name"] == model_name
                and item["image_index"] == image_index
            )
        ]

        await state.update_data(process_images_steps=process_images_steps)

    redis_storage = get_redis_storage()
    await redis_storage.delete_task(
        settings.PROCESS_IMAGE_TASK,
        key_for_image(call.from_user.id, image_index, model_name),
    )

    return True
