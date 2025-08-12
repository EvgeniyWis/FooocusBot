import asyncio
import os
from datetime import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext
from PIL import Image

from bot.app.config.constants import FACEFUSION_TEMP_IMAGES_FOLDER_PATH
from bot.helpers import text
from bot.helpers.generateImages.dataArray import get_model_index_by_model_name
from bot.helpers.handlers.messages import send_progress_message
from bot.helpers.jobs.get_job_id_by_model_name import get_job_id_by_model_name
from bot.app.core.logging import logger
from bot.utils import retryOperation
from bot.utils.facefusion import facefusion_swap
from bot.utils.handlers import appendDataToStateArray, deleteDataFromStateArray
from bot.utils.handlers.messages import editMessageOrAnswer


async def process_faceswap_image(
    call: types.CallbackQuery,
    state: FSMContext,
    image_index: int,
    model_name: str,
    model_key: str = None,
) -> str:
    """
    Функция для обработки замены лица, обработки процесса в хендлере, циклической проверки очереди на замену лица
    и удаления модели из стейта

    Attributes:
        call (types.CallbackQuery): callback-запрос
        state (FSMContext): контекст состояния
        image_index (int): индекс изображения
        model_name (str): название модели

    Returns:
        result_path (str): путь к результату замены лица
    """

    # Получаем айдишник пользователя
    user_id = call.from_user.id

    # Получаем индекс модели
    model_name_index = get_model_index_by_model_name(model_name)

    # Получаем job_id для текущей модели и индекса
    job_id = await get_job_id_by_model_name(state, model_name, model_key)
    temp_user_dir = FACEFUSION_TEMP_IMAGES_FOLDER_PATH / f"{job_id}"
    local_faceswap_target_path = os.path.join(
        str(FACEFUSION_TEMP_IMAGES_FOLDER_PATH),
        f"{job_id}",
        f"{image_index}.jpg",
    )
    logger.info(
        f"[faceswap] START: {local_faceswap_target_path} "
        f"exists={os.path.exists(local_faceswap_target_path)} | "
        f"dir={os.listdir(temp_user_dir) if temp_user_dir.exists() else 'NO_DIR'}",
    )
    # Путь для передачи в facefusion_swap (виден внутри facefusion-контейнера)
    faceswap_target_path = f"/facefusion/.assets/images/temp/{job_id}/{image_index}.jpg"
    faceswap_source_path = (
        f"/facefusion/.assets/images/faceswap/{model_name}.jpg"
    )
    logger.info(
        f"Путь к исходному изображению для замены лица: {faceswap_target_path}",
    )
    logger.info(
        f"Путь к целевому изображению для замены лица: {faceswap_source_path}",
    )

    # Добавляем в стейт путь к изображению для faceswap
    data_for_update = {
        "user_id": user_id,
        "image_index": image_index,
        "model_name": model_name,
    }
    await appendDataToStateArray(
        state,
        "faceswap_generated_models",
        data_for_update,
    )

    # Запускаем цикл, что пока очередь генераций не освободится, то ответ не будет выдан и генерацию не начинаем
    start_time = datetime.now()
    last_models_state = []
    error_message = None

    result_path = None

    while True:
        state_data = await state.get_data()
        faceswap_generated_models = state_data.get(
            "faceswap_generated_models",
            [],
        )

        # Проверяем, изменился ли список моделей
        if len(faceswap_generated_models) != len(last_models_state):
            start_time = datetime.now()
            last_models_state = faceswap_generated_models.copy()

        # Проверяем таймаут
        current_time = datetime.now()
        elapsed_time = (current_time - start_time).total_seconds()
        if elapsed_time > 1800:  # 30 минут = 1800 секунд
            error_message = f"Время ожидания замены лица для модели {model_name} истекло!"
            logger.error(
                error_message,
            )
            break

        # Если список пуст, то завершаем цикл
        if not len(faceswap_generated_models):
            break

        # Если в списке генераций настала очередь этой модели, то запускаем генерацию
        if model_name == faceswap_generated_models[0]["model_name"]:
            # Удаляем из стейта данные о ожидании замены лица
            await deleteDataFromStateArray(
                state,
                "faceswap_generation_wait_messages",
                model_name,
                "model_name",
            )

            try:
                if temp_user_dir.exists():
                    logger.info(
                        f"[process_faceswap_image] Содержимое папки {temp_user_dir}: {os.listdir(temp_user_dir)}",
                    )
                else:
                    logger.warning(
                        f"[process_faceswap_image] Папка {temp_user_dir} не существует!",
                    )

                # Проверяем, существует ли файл для faceswap до запуска
                logger.info(
                    f"[process_faceswap_image] Проверка файла: "
                    f"{local_faceswap_target_path} exists={os.path.exists(local_faceswap_target_path)}",
                )
                if not os.path.exists(local_faceswap_target_path):
                    logger.error(
                        f"[process_faceswap_image] Файл не найден: {local_faceswap_target_path} "
                        f"(model={model_name}, image_index={image_index}, user_id={user_id})",
                    )
                    await editMessageOrAnswer(
                        call,
                        f"❌ Изображение для upscale и замены лица не найдено! (model={model_name}, image_index={image_index})",
                    )
                    return None

                # PIL check: Проверяем валидность изображения
                try:
                    with Image.open(local_faceswap_target_path) as img:
                        img.verify()
                except Exception as pil_exc:
                    logger.error(
                        f"[process_faceswap_image] Файл невалиден или поврежден "
                        f"для faceswap: {local_faceswap_target_path} (model={model_name},"
                        f" image_index={image_index}, user_id={user_id}) — {pil_exc}",
                    )
                    await editMessageOrAnswer(
                        call,
                        f"❌ Изображение повреждено или невалидно для замены лица! "
                        f"(model={model_name}, image_index={image_index})",
                    )
                    return None
                logger.info(
                    f"[process_faceswap_image] Путь для FaceFusion в контейнере: {faceswap_target_path}",
                )
                # Копирование больше не требуется, так как файл уже в нужном месте
                result_path = await retryOperation(
                    facefusion_swap,
                    3,
                    2,
                    faceswap_source_path,
                    faceswap_target_path,
                )
            except Exception as e:
                result_path = None
                logger.error(
                    f"Произошла ошибка при замене лица у модели {model_name} с индексом {model_name_index}: {e}",
                )
                await editMessageOrAnswer(
                    call,
                    text.FACE_SWAP_ERROR_TEXT.format(
                        model_name,
                        model_name_index,
                        str(e)[0:100],
                    ),
                )
                error_message = e

            break

        await asyncio.sleep(10)

    # Удаляем из стейта данные о прогрессе faceswap
    await deleteDataFromStateArray(
        state,
        "faceswap_generation_wait_messages",
        model_name,
        "model_name",
    )

    # После генерации удаляем модель из стейта
    logger.info(
        f"[faceswap] END: {local_faceswap_target_path} exists={os.path.exists(local_faceswap_target_path)}"
        f" | dir={os.listdir(temp_user_dir) if temp_user_dir.exists() else 'NO_DIR'}",
    )
    await asyncio.sleep(5)
    logger.info(
        "Ждем 5 секунд, чтобы модель успела нормально сохраниться и отдать ресурсы",
    )
    # После генерации удаляем модель из стейта по model_name и image_index
    state_data = await state.get_data()
    faceswap_generated_models = state_data.get("faceswap_generated_models", [])
    faceswap_generated_models_without_current = [
        model
        for model in faceswap_generated_models
        if not (
            model["model_name"] == model_name
            and model["image_index"] == image_index
        )
    ]
    await state.update_data(
        faceswap_generated_models=faceswap_generated_models_without_current,
    )

    if error_message:
        data_for_update = {
            "model_name": model_name,
            "image_index": image_index,
        }
        await appendDataToStateArray(
            state,
            "faceswap_errors",
            data_for_update,
        )
        raise Exception(error_message)

    return result_path
