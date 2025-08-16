import re

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.app.core.logging import logger
from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    get_model_index_by_model_name,
    getDataByModelName,
)
from bot.helpers.generateImages.generateImageBlock import generateImageBlock
from bot.utils.handlers import getDataInDictsArray
from bot.utils.handlers.messages.editMessageOrAnswer import editMessageOrAnswer


async def get_normal_model(model_name: str) -> str:
    split_model_name = model_name.split("+")[0]
    re_model_name = re.sub(r"_\d+$", "", split_model_name)
    return re_model_name


# Функция для перегенерации изображения
async def regenerateImage(
    model_name: str,
    call: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()

    # Получаем индекс модели
    model_name_index = get_model_index_by_model_name(
        await get_normal_model(model_name),
    )

    user_id = call.from_user.id

    # Отправляем сообщение о перегенерации изображения
    regenerate_message = await editMessageOrAnswer(
        call,
        text.REGENERATE_IMAGE_TEXT.format(
            await get_normal_model(model_name),
            model_name_index,
        ),
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
    logger.info(
        f"Промпты для перегенерации изображения: {prompts_for_models}",
    )
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

    # Преобразуем возможный full_model_key в базовое имя модели
    full_model_key = model_name
    if "/" in full_model_key:
        base_model_name, _ = full_model_key.rsplit("/", 1)
    else:
        base_model_name = full_model_key

    normal_model_name = await get_normal_model(base_model_name)
    # Получаем данные генерации по названию модели
    data = await getDataByModelName(normal_model_name)

    if not data:
        logger.error(f"[regenerateImage] Не найдены данные для модели: {normal_model_name} (исходный ключ: {full_model_key})")
        await editMessageOrAnswer(
            call,
            text.REGENERATE_IMAGE_ERROR_TEXT.format(
                normal_model_name,
                model_name_index,
                "Модель не найдена",
            ),
        )
        try:
            await regenerate_message.delete()
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения о перегенерации изображения: {e}")
        return

    try:
        result, _ = await generateImageBlock(
            data,
            call.message.message_id,
            state,
            user_id,
            prompt,
            False,
            chat_id=call.message.chat.id,
        )

        if not result:
            raise Exception("Ошибка обработки на RunPod!")
    except Exception as e:
        logger.error(f"Ошибка при перегенерации изображения: {e}")
        await editMessageOrAnswer(
            call,
            text.REGENERATE_IMAGE_ERROR_TEXT.format(
                model_name,
                model_name_index,
                e,
            ),
        )
    finally:
        try:
            await regenerate_message.delete()
        except Exception as e:
            logger.error(
                f"Ошибка при удалении сообщения о перегенерации изображения: {e}",
            )
