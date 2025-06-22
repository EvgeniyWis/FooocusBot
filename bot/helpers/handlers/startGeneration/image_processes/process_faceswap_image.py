import asyncio
from datetime import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.helpers import text
from bot.helpers.generateImages.dataArray import getModelNameIndex
from bot.logger import logger
from bot.utils.facefusion import facefusion_swap
from bot.utils.handlers import appendDataToStateArray
from bot.utils.handlers.messages import editMessageOrAnswer
from bot.utils.retryOperation import retryOperation


async def process_faceswap_image(
    call: types.CallbackQuery,
    state: FSMContext,
    image_index: int,
    model_name: str,
) -> str:
    """
    Функция для обработки замены лица, обработки процесса в хендлере, циклической проверки очереди на замену лица
    и удаления модели из стейта

    Attributes:
        call (types.CallbackQuery): callback-запрос
        state (FSMContext): контекст состояния
        image_index (int): индекс изображения
        model_name (str): название модели
    """

    # Получаем айдишник пользователя
    user_id = call.from_user.id

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Меняем текст на сообщении об очереди на замену лица
    await editMessageOrAnswer(
        call,
        text.FACE_SWAP_WAIT_TEXT.format(model_name, model_name_index),
    )

    # Заменяем лицо на исходном изображении, которое сгенерировалось, на лицо с изображения модели
    faceswap_target_path = (
        f"images/temp/{model_name}_{user_id}/{image_index}.jpg"
    )
    faceswap_source_path = f"images/faceswap/{model_name}.jpg"
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
            "faceswap_generated_models", [],
        )

        # Проверяем, изменился ли список моделей
        if len(faceswap_generated_models) != len(last_models_state):
            start_time = datetime.now()
            last_models_state = faceswap_generated_models.copy()

        # Проверяем таймаут
        current_time = datetime.now()
        elapsed_time = (current_time - start_time).total_seconds()
        if elapsed_time > 1200:  # 20 минут = 1200 секунд
            error_message = f"Таймаут ожидания обновления списка faceswap_generated_models для модели {model_name}"
            logger.error(
                error_message,
            )
            break

        logger.info(
            f"Список генераций для замены лица: {faceswap_generated_models}",
        )

        # Если список пуст, то завершаем цикл
        if not len(faceswap_generated_models):
            break

        # Если в списке генераций настала очередь этой модели, то запускаем генерацию
        if model_name == faceswap_generated_models[0]["model_name"]:
            await editMessageOrAnswer(
                call,
                text.FACE_SWAP_PROGRESS_TEXT.format(
                    image_index,
                    model_name,
                    model_name_index,
                ),
            )

            try:
                result_path = await retryOperation(
                    facefusion_swap,
                    5,
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
                        e,
                    ),
                )
                error_message = e

            break

        await asyncio.sleep(10)

    # После генерации удаляем модель из стейта
    state_data = await state.get_data()
    faceswap_generated_models = state_data.get("faceswap_generated_models", [])
    faceswap_generated_models_without_current_model = [
        model
        for model in faceswap_generated_models
        if model["model_name"] != model_name
    ]
    await state.update_data(
        faceswap_generated_models=faceswap_generated_models_without_current_model,
    )

    if error_message:
        raise Exception(error_message)

    return result_path
