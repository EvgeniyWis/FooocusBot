from aiogram.fsm.context import FSMContext
from bot.helpers.handlers.startGeneration.image_processes.process_image_steps import ProcessImageStep

async def update_process_image_step(
    state: FSMContext, 
    model_name: str, 
    new_step: ProcessImageStep
) -> None:
    """
    Функция обновляет шаг обработки изображения для модели в массиве process_images_steps для state.
    Всего есть 3 этапа обработки: upscale, faceswap, save.

    Attributes:
        - state: FSMContext, контекст состояния
        - model_name: str, название модели
        - new_step: ProcessImageStep, новый шаг обработки изображения (upscale, faceswap, save)
    """

    state_data = await state.get_data()
    process_images_steps = state_data.get("process_images_steps", [])
    for item in process_images_steps:
        if item["model_name"] == model_name:
            item["step"] = new_step

    await state.update_data(process_images_steps=process_images_steps)

    return new_step