from aiogram import types
from aiogram.fsm.context import FSMContext

from ...generateImages.dataArray import getSettingNumberByModelName
from .sendImageBlock import sendImageBlock
from .waitStateArrayReplenishment import waitStateArrayReplenishment


# Функция для ожидания следующих блоков изображений и последующей отправки
async def waitForImageBlocksGeneration(
    message: types.Message, state: FSMContext, user_id: int,
) -> str:
    # Ждём пока появится следующий блок изображений в очереди
    media_groups_for_generation = await waitStateArrayReplenishment(
        state,
        "media_groups_for_generation",
        ("will_be_sent_generated_images_count", "total_images_count"),
    )

    if not media_groups_for_generation:
        return ""

    # Определение переменной stateData перед использованием
    stateData = await state.get_data()

    # Проверяем тестовая ли генерация
    is_test_generation = stateData["generations_type"] == "test"

    # Получаем следующий блок изображений в очереди
    media_group = media_groups_for_generation[0]
    model_name = list(media_group.keys())[0]
    media_group = media_group[model_name]

    # Добавляем эту модель в "очередь генерации"
    stateData["models_for_generation_queue"].append(model_name)
    await state.update_data(
        models_for_generation_queue=stateData["models_for_generation_queue"],
    )

    # Получаем номер настройки
    setting_number = getSettingNumberByModelName(model_name)

    # Отправляем изображение
    await sendImageBlock(
        message,
        state,
        media_group,
        model_name,
        setting_number,
        is_test_generation,
        user_id,
    )

    # Удаляем блок изображений из очереди
    await state.update_data(
        media_groups_for_generation=media_groups_for_generation[1:],
    )

    return model_name
