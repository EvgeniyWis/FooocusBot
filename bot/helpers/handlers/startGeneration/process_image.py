import os

from adapters.redis_task_storage_repository import key_for_image
from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.assets.mocks.links import MOCK_FACEFUSION_PATH
from bot.constants import TEMP_FOLDER_PATH
from bot.domain.entities.task import TaskProcessImageDTO
from bot.helpers import text
from bot.helpers.handlers.startGeneration.image_processes import (
    ProcessImageStep,
    get_current_process_image_step,
    process_faceswap_image,
    process_save_image,
    process_upscale_image,
    update_process_image_step,
)
from bot.helpers.jobs.get_job_id_by_model_name import get_job_id_by_model_name
from bot.keyboards.startGeneration import keyboards
from bot.logger import logger
from bot.settings import settings
from bot.storage import get_redis_storage
from bot.utils import retryOperation
from bot.utils.error_notifier import send_error_to_developers_with_callback
from bot.utils.handlers import (
    appendDataToStateArray,
    getDataInDictsArray,
)
from bot.utils.handlers.messages import safe_send_message


async def process_image(
    call: types.CallbackQuery,
    state: FSMContext,
    model_name: str,
    image_index: int,
    model_key: str = None,
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

    # Получаем job_id для текущей модели
    job_id = await get_job_id_by_model_name(state, model_name, model_key)
    if not job_id:
        raise Exception(f"Не найден job_id для model_name={model_name}")

    if not settings.MOCK_IMAGES_MODE:
        temp_image_path = (
            TEMP_FOLDER_PATH
            / f"{job_id}"
            / f"{image_index}.jpg"
        )
        if process_image_step == ProcessImageStep.UPSCALE:
            logger.info(
                f"[process_image] UPSCALE START: model_name={model_name}, image_index={image_index}, user_id={call.from_user.id}",
            )
            logger.info(
                f"[process_image] temp dir before UPSCALE: {os.listdir(TEMP_FOLDER_PATH / f'{job_id}') if (TEMP_FOLDER_PATH / f'{job_id}').exists() else 'NO_DIR'}",
            )
            logger.info(f"Запускаем upscale для ({model_name}, {image_index})")

            if settings.UPSCALE_MODE:
                try:
                    await retryOperation(
                        process_upscale_image,
                        3,
                        2,
                        call,
                        state,
                        image_index,
                        model_name,
                        False,  # is_second=False для первого апскейла
                        model_key,
                    )
                except Exception as e:
                    logger.error(f"[process_image] Ошибка при первом апскейле для ({model_name}, {image_index}): {e}")
                    # Отправляем ошибку разработчикам, но продолжаем обработку для пользователя
                    await send_error_to_developers_with_callback(
                        e, 
                        f"First upscale failed for ({model_name}, {image_index})", 
                        call
                    )

            logger.info(
                f"[process_image] UPSCALE END: model_name={model_name}, image_index={image_index}, user_id={call.from_user.id}, file exists={os.path.exists(temp_image_path)}",
            )
            logger.info(
                f"[process_image] temp dir after UPSCALE: {os.listdir(TEMP_FOLDER_PATH / f'{job_id}') if (TEMP_FOLDER_PATH / f'{job_id}').exists() else 'NO_DIR'}",
            )

            process_image_step = await update_process_image_step(
                state,
                model_name,
                image_index,
                ProcessImageStep.SECOND_UPSCALE,
            )

            if (
                settings.SECOND_UPSCALE_MODE
                and process_image_step == ProcessImageStep.SECOND_UPSCALE
            ):
                try:
                    await process_upscale_image(
                        call=call,
                        state=state,
                        image_index=image_index,
                        model_name=model_name,
                        is_second=True,
                        model_key=model_key,
                    )
                except Exception as e:
                    # Отправляем ошибку разработчикам, но продолжаем обработку для пользователя
                    await send_error_to_developers_with_callback(
                        e, 
                        f"Second upscale failed for ({model_name}, {image_index})", 
                        call
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

        if process_image_step == ProcessImageStep.FACEFUSION:
            logger.info(
                f"[process_image] FACEFUSION START: model_name={model_name}, image_index={image_index}, user_id={call.from_user.id}",
            )
            faceswap_target_path = temp_image_path
            logger.info(
                f"[process_image] Проверка файла перед faceswap: {faceswap_target_path} exists={os.path.exists(faceswap_target_path)}",
            )
            logger.info(
                f"[process_image] temp dir before FACEFUSION: {os.listdir(TEMP_FOLDER_PATH / f'{job_id}') if (TEMP_FOLDER_PATH / f'{job_id}').exists() else 'NO_DIR'}",
            )
            if not os.path.exists(faceswap_target_path):
                logger.warning(
                    f"[process_image] Файл не найден для faceswap: {faceswap_target_path}",
                )
                return False

            if settings.FACEFUSION_MODE:
                result_path = await process_faceswap_image(
                    call,
                    state,
                    image_index,
                    model_name,
                    model_key=model_key,
                )
            else:
                result_path = MOCK_FACEFUSION_PATH

            logger.info(
                f"[process_image] FACEFUSION END: model_name={model_name}, image_index={image_index}, user_id={call.from_user.id}, file exists={os.path.exists(faceswap_target_path)}",
            )
            logger.info(
                f"[process_image] temp dir after FACEFUSION: {os.listdir(TEMP_FOLDER_PATH / f'{job_id}') if (TEMP_FOLDER_PATH / f'{job_id}').exists() else 'NO_DIR'}",
            )
            if result_path:
                await state.update_data(
                    {f"{model_name}_{image_index}_result_path": str(result_path)},
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
        direct_url = await process_save_image(
            call,
            state,
            model_name,
            image_index,
            result_path=result_path,
            model_key=model_key,
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

        saved_images_urls = state_data.get("saved_images_urls", [])

        saved_image_url = await getDataInDictsArray(
            saved_images_urls,
            model_name,
            image_index,
        )

        if not saved_image_url:
            data_for_update = {
                "model_name": model_name,
                "image_index": image_index,
                "direct_url": direct_url,
            }
            await appendDataToStateArray(
                state,
                "saved_images_urls",
                data_for_update,
                unique_keys=("model_name", "image_index"),
            )

    redis_storage = get_redis_storage()
    await redis_storage.delete_task(
        settings.PROCESS_IMAGE_TASK,
        key_for_image(call.from_user.id, image_index, model_name),
    )

    # Получаем стейт и если кол-во сохраненных изображений равно количеству изображений, то отправляем сообщение с возможностью генерации видео по 1 промпту
    state_data = await state.get_data()
    saved_images_urls = state_data.get("saved_images_urls", [])
    total_jobs_count = state_data.get("total_jobs_count", 0)

    if len(saved_images_urls) == total_jobs_count > 1:
        await safe_send_message(
            text.ALL_IMAGES_SUCCESSFULLY_SAVED_TEXT,
            call.message,
            reply_markup=keyboards.all_images_successfully_saved_keyboard(),
        )

    return True
