from aiogram import types
from aiogram.fsm.context import FSMContext
from logger import logger

from ... import text
from ...generateImages import generateImageBlock
from ...generateImages.dataArray import getDataByModelName, getModelNameIndex
from ...handlers.appendDataToStateArray import appendDataToStateArray
from ..editMessageOrAnswer import editMessageOrAnswer


# Функция для перегенерации изображения
async def regenerateImage(model_name: str, call: types.CallbackQuery, state: FSMContext, setting_number: str):
    stateData = await state.get_data()
    is_test_generation = stateData["generations_type"] == "test"

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Получаем id пользователя
    user_id = call.from_user.id

    # Отправляем сообщение о перегенерации изображения
    await editMessageOrAnswer(
    call, text.REGENERATE_IMAGE_TEXT.format(model_name, model_name_index))

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    # Получаем промпт для перегенерации изображения
    try:
        prompt = stateData["prompts_for_regenerate_images"][model_name]
        logger.info(f"Промпт для перегенерации изображения: {prompt}")
    except Exception as e:
        logger.error(f"Произошла ошибка при получении промпта для перегенерации изображения: {e}")
        prompt = stateData["prompt_for_images"]

    # Прибавляем к каждому элементу массива корневой промпт
    data["json"]['input']['prompt'] += " " + prompt

    return await generateImageBlock(data["json"], model_name, call.message, state, user_id, setting_number, is_test_generation, False)
