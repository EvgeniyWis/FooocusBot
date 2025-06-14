from aiogram.fsm.context import FSMContext
from bot.helpers.handlers.startGeneration.image_processes.process_image_steps import ProcessImageStep
from bot.utils.handlers import appendDataToStateArray


async def get_current_process_image_step(state: FSMContext, model_name: str) -> ProcessImageStep:
    """
    Функция определяет текущий этап обработки изображения для модели из массива process_images_steps из state.
    Если текущей модели ещё нет в массиве, то добавляет её и инициализирует начальный этап - upscale.
    Если же модель уже есть в массиве, то получает её текущий этап обработки.

    Attributes:
        - state: FSMContext, контекст состояния
        - model_name: str, название модели

    Returns:
        - ProcessImageStep: текущий этап обработки изображения
    """
    # Если текущей модели ещё нет в массиве "process_images_steps", то добавляем её
    state_data = await state.get_data()
    process_images_steps = state_data.get("process_images_steps", [])
    model_names_in_process_images_steps = [item["model_name"] for item in process_images_steps]

    if model_name not in model_names_in_process_images_steps:
        process_image_step = ProcessImageStep.UPSCALE # Начинаем с upscale
        data_for_update = {"model_name": model_name, "step": process_image_step}
        await appendDataToStateArray(state, "process_images_steps", data_for_update)

    # Если же модель уже есть в массиве, то получаем её текущий этап обработки
    else: 
        process_image_step = [item["step"] for item in process_images_steps if item["model_name"] == model_name][0]

    return ProcessImageStep(process_image_step)