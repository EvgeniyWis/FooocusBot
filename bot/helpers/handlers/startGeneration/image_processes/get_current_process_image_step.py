from aiogram.fsm.context import FSMContext

from bot.helpers.handlers.startGeneration.image_processes.process_image_steps import (
    ProcessImageStep,
)
from bot.utils.handlers import appendDataToStateArray


async def get_current_process_image_step(
    state: FSMContext, model_name: str, image_index: int
) -> ProcessImageStep:
    """
    Функция определяет текущий этап обработки изображения для конкретной картинки (model_name, image_index)
    из массива process_images_steps из state.
    Если такой записи нет, добавляет и инициализирует начальный этап - upscale.
    """
    state_data = await state.get_data()
    process_images_steps = state_data.get("process_images_steps", [])
    for item in process_images_steps:
        if (
            item["model_name"] == model_name
            and item["image_index"] == image_index
        ):
            return ProcessImageStep(item["step"])
    process_image_step = ProcessImageStep.UPSCALE
    data_for_update = {
        "model_name": model_name,
        "image_index": image_index,
        "step": process_image_step,
    }
    await appendDataToStateArray(
        state, "process_images_steps", data_for_update
    )
    return process_image_step
