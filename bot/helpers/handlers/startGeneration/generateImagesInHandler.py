import traceback

from aiogram import types
from aiogram.fsm.context import FSMContext
from InstanceBot import bot
from utils.handlers.messages import safe_edit_message

from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    get_data_array_by_group_number,
    get_model_index_by_model_name,
    get_model_index_in_group,
)
from bot.helpers.generateImages.dataArray.get_data_array_by_model_indexes import (
    get_data_array_by_model_indexes,
)
from bot.helpers.generateImages.generate_images_by_all_groups import (
    generate_images_by_all_groups,
)
from bot.helpers.generateImages.generateImageBlock import generateImageBlock
from bot.helpers.generateImages.generateImages import generateImages
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

        if group_number == "all":
            result = await generate_images_by_all_groups(
                message_for_edit,
                state,
                user_id,
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

                logger.info(f"[generateImagesInHandler] dataArray: {dataArray}")

                for data in dataArray:
                    if group_number != "individual":
                        model_index = get_model_index_in_group(data["model_index"], group_number)
                    else:
                        model_index = get_model_index_by_model_name(data["model_name"])
                    prompt_for_current_model[str(model_index)] = prompt

                result = await generateImages(
                    group_number=group_number,
                    prompt_for_current_model=prompt_for_current_model,
                    message=message_for_edit,
                    state=state,
                    user_id=user_id,
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

            await safe_send_message(
                text.ASK_FOR_NEW_GENERATION_TEXT,
                message,
                reply_markup=start_generation_keyboards.generationsTypeKeyboard(
                    with_video_from_image_generation=False,
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
