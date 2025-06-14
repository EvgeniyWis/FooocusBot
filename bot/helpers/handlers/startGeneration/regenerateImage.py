from aiogram import types
from aiogram.fsm.context import FSMContext
from logger import logger

from bot.helpers import text
from bot.helpers.generateImages import generateImageBlock
from bot.helpers.generateImages.dataArray import (
    getDataByModelName,
    getModelNameIndex,
)
from bot.utils.handlers import getDataInDictsArray
from bot.utils.handlers.messages.editMessageOrAnswer import editMessageOrAnswer


# Функция для перегенерации изображения
async def regenerateImage(
    model_name: str,
    call: types.CallbackQuery,
    state: FSMContext,
    setting_number: str,
):
    stateData = await state.get_data()
    is_test_generation = stateData.get("generations_type", "") == "test"

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Получаем id пользователя
    user_id = call.from_user.id

    # Отправляем сообщение о перегенерации изображения
    regenerate_message = await editMessageOrAnswer(
        call, text.REGENERATE_IMAGE_TEXT.format(model_name, model_name_index)
    )

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    # Получаем промпт для перегенерации изображения в зависимости от режима генерации
    randomizer_prompts = stateData.get("randomizer_prompts", [])
    randomizer_prompt = await getDataInDictsArray(
        randomizer_prompts, model_name
    )
    prompt_for_images = stateData.get("prompt_for_images", "")
    prompts_for_regenerated_models = stateData.get(
        "prompts_for_regenerated_models", []
    )
    prompt_for_regenerate_image = await getDataInDictsArray(
        prompts_for_regenerated_models, model_name
    )

    if prompt_for_regenerate_image:
        prompt = prompt_for_regenerate_image

        logger.info(f"Промпт для перегенерации изображения: {prompt}")

    elif randomizer_prompt:
        prompt = randomizer_prompt
        logger.info(
            f"Промпт для перегенерации изображения, полученный из рандомайзера: {prompt}"
        )

    elif prompt_for_images:
        prompt = prompt_for_images
        logger.info(
            f"Промпт для перегенерации изображения, полученный из стейта: {prompt}"
        )

    else:
        prompt = ""

    # Прибавляем к каждому элементу массива корневой промпт
    json = data["json"].copy()
    json["input"]["prompt"] += " " + prompt

    try:
        return await generateImageBlock(
            json,
            model_name,
            call.message.message_id,
            state,
            user_id,
            setting_number,
            is_test_generation,
            False,
            chat_id=call.message.chat.id,
        )
    finally:
        await regenerate_message.delete()
