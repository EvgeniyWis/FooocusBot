from aiogram import types
from aiogram.fsm.context import FSMContext
from logger import logger

from ... import text
from ...generateImages import generateImageBlock
from ...generateImages.dataArray import getDataByModelName, getModelNameIndex
from ..editMessageOrAnswer import editMessageOrAnswer
from utils.handlers import getDataInDictsArray


# Функция для перегенерации изображения
async def regenerateImage(model_name: str, call: types.CallbackQuery, state: FSMContext, setting_number: str):
    stateData = await state.get_data()
    is_test_generation = stateData.get("generations_type", "test") == "test"

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Получаем id пользователя
    user_id = call.from_user.id

    # Отправляем сообщение о перегенерации изображения
    await editMessageOrAnswer(
    call, text.REGENERATE_IMAGE_TEXT.format(model_name, model_name_index))

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    # Получаем промпт для перегенерации изображения в зависимости от режима генерации
    randomizer_prompts = stateData.get("randomizer_prompts", [])
    randomizer_prompt = await getDataInDictsArray(randomizer_prompts, model_name)
    prompt_for_images = stateData.get("prompt_for_images", "")
    prompts_for_regenerate_images = stateData.get("prompts_for_regenerate_images", [])
    prompts_for_regenerate_image = await getDataInDictsArray(prompts_for_regenerate_images, model_name)

    if prompts_for_regenerate_images:
        prompt = prompts_for_regenerate_image

        logger.info(f"Промпт для перегенерации изображения: {prompt}")

    elif randomizer_prompts:
        prompt = randomizer_prompt
        logger.info(f"Промпт для перегенерации изображения, полученный из рандомайзера: {prompt}")

    else:
        prompt = prompt_for_images
        logger.info(f"Промпт для перегенерации изображения, полученный из стейта: {prompt}")

    # Прибавляем к каждому элементу массива корневой промпт
    data["json"]['input']['prompt'] += " " + prompt

    return await generateImageBlock(data["json"], model_name, call.message, state, user_id, setting_number, is_test_generation, False)
