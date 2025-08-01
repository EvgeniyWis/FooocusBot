import traceback

from aiogram import types
from aiogram.fsm.context import FSMContext
from InstanceBot import bot
from utils.handlers.messages import safe_edit_message

from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    get_data_array_by_group_number,
    getModelNameIndex,
)
from bot.helpers.generateImages.generateImageBlock import generateImageBlock
from bot.helpers.generateImages.generateImages import generateImages
from bot.helpers.generateImages.generateImagesByAllSettings import (
    generateImagesByAllSettings,
)
from bot.helpers.generateImages.get_data_array_by_model_indexes import (
    get_data_array_by_model_indexes,
)
from bot.helpers.handlers.startGeneration.cancelImageGenerationJobs import (
    cancelImageGenerationJobs,
)
from bot.keyboards.startGeneration import (
    keyboards as start_generation_keyboards,
)
from bot.logger import logger
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)


# Функция для генерации изображения в зависимости от настроек
async def generateImagesInHandler(
    prompt: str | dict,
    message: types.Message,
    state: FSMContext,
    user_id: int,
    is_test_generation: bool,
    group_number: str,
    with_randomizer: bool = False,
):
    data = await state.get_data()
    if data.get("message_to_del"):
        try:
            await bot.delete_message(
                message.chat.id,
                data["message_to_del"],
            )
        except Exception:
            logger.warning(
                f"Не удалось удалить сообщение бота: {data['message_to_del']}",
            )

    message_for_edit = await safe_send_message(
        text=text.CANCEL_PREVIOUS_JOBS_TEXT,
        message=message,
    )

    await cancelImageGenerationJobs(state)

    try:
        state_data = await state.get_data()
        model_indexes_for_generation = state_data.get(
            "model_indexes_for_generation",
            [],
        )

        logger.info(
            f"Получен список моделей для индивидуальной генерации: {model_indexes_for_generation}",
        )

        if is_test_generation:
            if group_number == "all":
                result = await generateImagesByAllSettings(
                    message_for_edit,
                    state,
                    user_id,
                    is_test_generation,
                    prompt,
                )
            else:
                await safe_edit_message(
                    message_for_edit,
                    text.GET_PROMPT_SUCCESS_TEXT,
                )
                dataArray = get_data_array_by_group_number(group_number)
                data = dataArray[0]
                result = [
                    await generateImageBlock(
                        data,
                        message_for_edit.message_id,
                        state,
                        user_id,
                        group_number,
                        prompt if isinstance(prompt, str) else "",  # fallback
                        is_test_generation,
                        chat_id=message.chat.id,
                    ),
                ]
        else:
            if group_number == "all":
                result = await generateImagesByAllSettings(
                    message_for_edit,
                    state,
                    user_id,
                    is_test_generation,
                    prompt if isinstance(prompt, str) else "",
                    with_randomizer,
                )
            else:
                await message_for_edit.edit_text(text.GET_PROMPT_SUCCESS_TEXT)
                await message_for_edit.pin()

                if isinstance(prompt, dict):
                    model_indexes_for_generation = list(prompt.keys())

                    result = await generateImages(
                        group_number="individual",
                        prompt_for_current_model=prompt,
                        message=message_for_edit,
                        state=state,
                        user_id=user_id,
                        is_test_generation=is_test_generation,
                        with_randomizer=False,
                        model_indexes_for_generation=model_indexes_for_generation,
                    )
                else:
                    # Формируем словарь model_name -> prompt
                    prompt_for_current_model = {}

                    if group_number != "individual":
                        dataArray = get_data_array_by_group_number(group_number)
                    else:
                        dataArray = await get_data_array_by_model_indexes(
                            model_indexes_for_generation,
                        )

                    for data in dataArray:
                        model_index = getModelNameIndex(data["model_name"])
                        prompt_for_current_model[str(model_index)] = prompt

                    result = await generateImages(
                        group_number=group_number,
                        prompt_for_current_model=prompt_for_current_model,
                        message=message_for_edit,
                        state=state,
                        user_id=user_id,
                        is_test_generation=is_test_generation,
                        with_randomizer=with_randomizer,
                        model_indexes_for_generation=model_indexes_for_generation,
                    )

                await message_for_edit.unpin()

        state_data = await state.get_data()
        stop_generation = state_data.get("stop_generation", False)

        if not result and not stop_generation:
            raise Exception("Не получилось сгенерировать изображения!")
        else:
            state_data = await state.get_data()
            stop_generation = state_data.get("stop_generation", False)

            if not stop_generation and (
                len(model_indexes_for_generation) > 1
                or len(model_indexes_for_generation) == 0
            ):
                await safe_send_message(text.GENERATION_SUCCESS_TEXT, message)

            await safe_send_message(
                text.ASK_FOR_NEW_GENERATION_TEXT,
                message,
                reply_markup=start_generation_keyboards.generationsTypeKeyboard(
                    with_video_from_image_generation=False,
                    with_test_generation=False,
                ),
            )

    except Exception as e:
        try:
            await message_for_edit.unpin()
        except Exception:
            pass
        logger.error(f"Ошибка при генерации изображения: {e}")
        traceback.print_exc()
        await safe_send_message(
            text.GENERATION_IMAGE_ERROR_TEXT.format(e),
            message,
        )
        raise e
