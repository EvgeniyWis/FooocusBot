
from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.assets.mocks.links import (
    MOCK_FACEFUSION_PATH,
)
from bot.config import FACEFUSION_MODE, MOCK_MODE, UPSCALE_MODE
from bot.logger import logger
from bot.helpers.handlers.startGeneration.image_processes import (
    process_save_image,
    process_upscale_image,
    process_faceswap_image,
    get_current_process_image_step,
    ProcessImageStep,
    update_process_image_step
)


async def process_image(call: types.CallbackQuery, state: FSMContext, model_name: str, image_index: int):
    """
    Обрабатывает изображение после выбора индекса среди сгенерированных изображений.
    Последовательно производит над выбранным изображением операции upscale, faceswap 
    и сохраняет результат на Google Drive.
    В стейте сохраняется каждый текущий шаг обработки изображения для его возобновления в случае ошибки.

    Attributes:
        - call: types.CallbackQuery, объект вызова
        - state: FSMContext, контекст состояния
        - model_name: str, название модели
        - image_index: int, индекс выбранного изображения

    Returns:
        - bool, True если изображение успешно обработано, False если нет
    """

    # Инициализируем результирующий путь
    result_path = None

    # Получаем текущий этап обработки изображения для модели
    process_image_step = await get_current_process_image_step(state, model_name)

    # Если не в режиме мока, то продолжаем генерацию
    if not MOCK_MODE:
        # Меняем текст на сообщении о начале upscale
        if UPSCALE_MODE and process_image_step == ProcessImageStep.UPSCALE:
            await process_upscale_image(
                call, state, image_index, model_name
            )

            # Меняем шаг обработки изображения на faceswap
            process_image_step = await update_process_image_step(state, model_name, ProcessImageStep.FACEFUSION)

        if FACEFUSION_MODE:
            if process_image_step == ProcessImageStep.FACEFUSION:
                result_path = await process_faceswap_image(
                    call, state, image_index, model_name
                )

                # Меняем шаг обработки изображения на save
                process_image_step = await update_process_image_step(state, model_name, ProcessImageStep.SAVE)

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

    return True