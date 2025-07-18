from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.helpers import text
from bot.helpers.generateImages.dataArray.getDataByModelName import (
    getDataByModelName,
)
from bot.helpers.generateImages.dataArray.getModelNameIndex import (
    getModelNameIndex,
)
from bot.helpers.generateImages.generateImageBlock import generateImageBlock
from bot.logger import logger
from bot.utils.handlers import getDataInDictsArray
from bot.utils.handlers.messages.editMessageOrAnswer import editMessageOrAnswer


# Функция для перегенерации изображения
async def regenerateImage(
    model_name: str,
    call: types.CallbackQuery,
    state: FSMContext,
    setting_number: str,
):
    state_data = await state.get_data()
    is_test_generation = state_data.get("generations_type", "") == "test"

    # Получаем индекс модели
    model_name_index = await getModelNameIndex(model_name, call.from_user.id)

    # Получаем id пользователя
    user_id = call.from_user.id

    # Отправляем сообщение о перегенерации изображения
    regenerate_message = await editMessageOrAnswer(
        call,
        text.REGENERATE_IMAGE_TEXT.format(model_name, model_name_index),
    )

    # Получаем промпт для перегенерации изображения в зависимости от режима генерации
    randomizer_prompts = state_data.get("randomizer_prompts", [])
    randomizer_prompt = await getDataInDictsArray(
        randomizer_prompts,
        model_name,
    )

    prompt_for_images = state_data.get("prompt_for_images", None)

    prompts_for_regenerated_models = state_data.get(
        "prompts_for_regenerated_models",
        [],
    )
    prompt_for_regenerate_image = await getDataInDictsArray(
        prompts_for_regenerated_models,
        model_name,
    )

    prompts_for_models = state_data.get("model_prompts_for_generation", [])
    prompt_for_model = await getDataInDictsArray(
        prompts_for_models,
        model_name,
    )

    logger.info(
        f"""Промпты для перегенерации изображения:
        prompt_for_regenerate_image: {prompt_for_regenerate_image}
        randomizer_prompt: {randomizer_prompt}
        prompt_for_images: {prompt_for_images}
        prompt_for_model: {prompt_for_model}
        """,
    )

    if prompt_for_regenerate_image:
        prompt = prompt_for_regenerate_image

        logger.info(f"Промпт для перегенерации изображения: {prompt}")

    elif randomizer_prompt:
        prompt = randomizer_prompt
        logger.info(
            f"Промпт для перегенерации изображения, полученный из рандомайзера: {prompt}",
        )

    elif prompt_for_images:
        prompt = prompt_for_images
        logger.info(
            f"Промпт для перегенерации изображения, полученный из стейта: {prompt}",
        )

    elif prompt_for_model:
        prompt = prompt_for_model
        logger.info(
            f"Промпт для перегенерации изображения, полученный из уникальных промптов для моделей: {prompt}",
        )

    else:
        raise Exception("Промпт для перегенерации изображения не найден")

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)

    try:
        return await generateImageBlock(
            data,
            call.message.message_id,
            state,
            user_id,
            setting_number,
            prompt,
            is_test_generation,
            False,
            chat_id=call.message.chat.id,
        )
    finally:
        await regenerate_message.delete()
