from aiogram.fsm.context import FSMContext
import asyncio
from .sendImageBlock import sendImageBlock
from aiogram import types
from utils.generateImages.dataArray.getSettingNumberByModelName import getSettingNumberByModelName
from logger import logger


# Функция для ожидания следующих блоков изображений и последующей отправки
async def waitForImageBlocksGeneration(message: types.Message, state: FSMContext) -> str:
    # Ждём пока появится следующий блок изображений в очереди
    while True:
        stateData = await state.get_data()
        media_groups_for_generation = stateData["media_groups_for_generation"]

        logger.info(f"Модели для генерации: {[list(i.keys())[0] for i in media_groups_for_generation]}")

        if len(media_groups_for_generation) > 0:
            break

        if stateData["sent_images_count"] == stateData["success_images_count"]:
            return False

        await asyncio.sleep(5)

    # Проверяем тестовая ли генерация
    is_test_generation = stateData["generations_type"] == "test"

    # Получаем следующий блок изображений в очереди
    media_group = media_groups_for_generation[0]
    model_name = list(media_group.keys())[0]
    media_group = media_group[model_name]

    # Добавляем эту модель в "очередь генерации"
    stateData = await state.get_data()
    stateData["models_for_generation_queue"].append(model_name)
    await state.update_data(models_for_generation_queue=stateData["models_for_generation_queue"])

    # Получаем номер настройки
    setting_number = getSettingNumberByModelName(model_name)

    # Отправляем изображение
    await sendImageBlock(message, state, media_group, model_name, setting_number, is_test_generation)

    # Удаляем блок изображений из очереди
    await state.update_data(media_groups_for_generation=media_groups_for_generation[1:])

    return model_name["result"]