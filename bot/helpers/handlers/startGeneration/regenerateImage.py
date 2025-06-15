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
    state_data = await state.get_data()
    is_test_generation = state_data.get("generations_type", "") == "test"

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Получаем id пользователя
    user_id = call.from_user.id

    # Отправляем сообщение о перегенерации изображения
    regenerate_message = await editMessageOrAnswer(
        call, text.REGENERATE_IMAGE_TEXT.format(model_name, model_name_index)
    )

    # Получаем промпт для перегенерации изображения в зависимости от режима генерации
    randomizer_prompts = state_data.get("randomizer_prompts", [])
    randomizer_prompt = await getDataInDictsArray(
        randomizer_prompts, model_name
    )
    prompt_for_images = state_data.get("prompt_for_images", "")
    prompts_for_regenerated_models = state_data.get(
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

    try:
        return await generateImageBlock(
            model_name,
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
