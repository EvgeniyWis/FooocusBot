import asyncio
import os

from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from utils.handlers.messages import safe_edit_message

import bot.constants as constants
from bot.domain.entities.video_generation import ProcessingStatus
from bot.factory.comfyui_video_service import get_video_service
from bot.helpers.handlers.videoGeneration import (
    process_write_prompt,
    saveVideo,
)
from bot.InstanceBot import bot, router
from bot.keyboards import video_generation_keyboards
from bot.logger import logger
from bot.states import StartGenerationState
from bot.utils import retryOperation
from bot.utils.handlers import appendDataToStateArray, getDataInDictsArray
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)
from bot.utils.videos.download_nsfw_video import (
    download_nsfw_videos,
)
from bot.utils.videos.generate_nsfw_video import generate_nsfw_video


async def quick_generate_nsfw_video(
    call: types.CallbackQuery,
    state: FSMContext,
):
    model_name = call.data.split("|")[1]
    image_index = int(call.data.split("|")[2])

    if not call.message.photo:
        logger.error(f"Для {model_name} не нашлось изображение в сообщении")
        await call.answer("Ошибка: не найдено изображение в сообщении")
        return

    photo = call.message.photo[-1]
    file_id = photo.file_id

    await state.update_data(
        image_file_id_for_nsfw_img2video=file_id,
    )

    await process_write_prompt(
        call,
        state,
        model_name,
        image_index,
        is_nsfw_generation=True,
    )


async def generate_nsfw_video_and_send_result(
    message_or_call: types.CallbackQuery | types.Message,
    state: FSMContext,
    prompt: str,
    temp_path: str,
    seconds: int = None,
):
    def get_target_message(
        message_or_call: types.CallbackQuery | types.Message,
    ):
        return (
            message_or_call.message
            if isinstance(message_or_call, types.CallbackQuery)
            else message_or_call
        )

    state_data = await state.get_data()
    model_name = state_data.get("model_name_for_video_generation", "")
    image_index = state_data.get("image_index_for_video_generation", None)

    progress_message = await safe_send_message(
        "⏳ Генерация NSFW видео через ComfyUI...",
        message_or_call.message
        if isinstance(message_or_call, types.CallbackQuery)
        else message_or_call,
    )

    status = await generate_nsfw_video(prompt, temp_path, seconds)
    prompt_id = None

    if status.status == "queued":
        prompt_id = status.prompt_id
        pos = status.position
        total = status.queue_length
        wait_min = status.wait_min

        if wait_min >= 150:
            msg = (
                f"🕒 Вы в очереди: {pos} из {total}.\n"
                f"Примерное ожидание: {int(wait_min)} мин.\n"
                f"🚫Очередь очень длинная, возможно, придётся ждать до 3 часов."
            )
        elif wait_min >= 80:
            msg = (
                f"🕒 Вы в очереди: {pos} из {total}.\n"
                f"Примерное ожидание: {int(wait_min)} мин.\n"
                f"🚫Очередь длинная. Ожидайте или попробуйте позже."
            )
        else:
            msg = (
                f"🕒 Вы в очереди: {pos} из {total}.\n"
                f"Примерное ожидание: {int(wait_min)} мин."
            )
        await safe_send_message(msg, get_target_message(message_or_call))

    elif status.status in ("start_generation", "processing"):
        prompt_id = status.prompt_id
        wait_min = status.wait_min
        await safe_send_message(
            f"⚙️ Генерация началась. Примерное ожидание: {int(wait_min)} мин.",
            get_target_message(message_or_call),
        )

    elif status.status == "timeout":
        await safe_send_message(
            "❌ Время ожидания начала генерации истекло. Попробуйте позже.",
            get_target_message(message_or_call),
        )
        await progress_message.delete()
        return

    elif status.status == "error":
        await safe_send_message(
            "❌ Произошла ошибка при генерации NSFW видео.",
            get_target_message(message_or_call),
        )
        await progress_message.delete()
        return

    else:
        logger.error(f"Неизвестный статус генерации: {status}")
        await progress_message.delete()
        return

    if not prompt_id:
        await safe_send_message(
            "❌ Не удалось получить идентификатор задачи генерации.",
            get_target_message(message_or_call),
        )
        await progress_message.delete()
        return

    video_service = get_video_service()

    result_final = None
    try:
        result_final = await video_service.wait_for_result(prompt_id)
    except Exception:
        try:
            result_final = await retryOperation(
                video_service.wait_for_result,
                5,
                5,
                prompt_id,
            )
        except Exception as e:
            await safe_send_message(
                f"❌ Ошибка во время ожидания результата: {e}",
                get_target_message(message_or_call),
            )
            await progress_message.delete()
            return

    if not result_final:
        await safe_send_message(
            "❌ Результат не получен. Скорее всего, ComfyUI не отвечает. Администрация уже уведомлена.",
            get_target_message(message_or_call),
        )
        return

    await progress_message.delete()

    if result_final.get("video_urls"):
        video_urls = result_final["video_urls"]
        await state.update_data(generated_nsfw_video_urls=video_urls)

        async for v, idx in download_nsfw_videos(video_urls):
            if not v.path:
                continue

            video = types.FSInputFile(v.path)
            await (
                message_or_call.message.answer_video
                if isinstance(
                    message_or_call,
                    types.CallbackQuery,
                )
                else message_or_call.answer_video
            )(video=video, caption=v.caption,
            reply_markup=video_generation_keyboards.videoCorrectnessKeyboard(
                model_name=model_name,
                image_index=image_index,
                is_nsfw=True,
            ))

            data_for_update = {
                "video_index": idx,
                "image_index": image_index,
                "model_name": model_name,
                "direct_url": v.path,
            }
            await appendDataToStateArray(
                state,
                "generated_nsfw_video_paths",
                data_for_update,
                unique_keys=("model_name", "image_index", "video_index"),
            )

            try:
                os.remove(v.path)
            except Exception as e:
                logger.error(
                    f"Ошибка при удалении временного файла {v.path}: {e}",
                )

        await state.set_state(None)
    elif result_final.get("error"):
        await safe_send_message(
            f"❌ Ошибка генерации: {result_final['error']}",
            get_target_message(message_or_call),
        )
    else:
        await safe_send_message(
            "❌ Не удалось получить результат от ComfyUI.",
            get_target_message(message_or_call),
        )

    try:
        os.remove(temp_path)
    except Exception:
        pass


async def handle_prompt_for_nsfw_generation(
    message: types.Message,
    state: FSMContext,
):
    prompt = message.text
    await state.update_data(prompt_for_nsfw_video=prompt)

    try:
        await message.delete()
    except Exception as e:
        logger.warning(
            f"Не удалось удалить сообщение пользователя с промптом: {e}",
        )

    state_data = await state.get_data()
    write_prompt_messages = state_data.get("write_prompt_messages_ids", [])
    model_name = state_data.get("model_name_for_video_generation")

    target_msg_id = None
    for entry in write_prompt_messages:
        if entry.get("model_name") == model_name:
            target_msg_id = entry.get("message_id")
            break

    if target_msg_id:
        try:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=target_msg_id,
            )
        except Exception as e:
            logger.warning(
                f"Не удалось удалить сообщение бота с запросом промпта: {e}",
            )

    state_data = await state.get_data()
    file_id = state_data.get("image_file_id_for_nsfw_img2video")

    if not file_id:
        await safe_send_message(
            "❌ Не найдено изображение для NSFW генерации.",
            message,
        )
        return

    temp_dir = constants.TEMP_IMAGE_FILES_DIR
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, f"{file_id}.jpg")

    try:
        file = await asyncio.wait_for(bot.get_file(file_id), timeout=30)
        await asyncio.wait_for(
            bot.download_file(file.file_path, temp_path),
            timeout=60,
        )
    except Exception as e:
        await safe_send_message(f"Ошибка скачивания изображения: {e}", message)
        return

    await state.update_data(temp_path_for_nsfw=temp_path)
    duration_msg = await safe_send_message(
        "⏳ Выберите способ задания длительности видео:",
        message,
        reply_markup=video_generation_keyboards.nsfw_video_generation_insert_length_video_keyboard(),
    )

    await state.update_data(duration_prompt_msg_id=duration_msg.message_id)
    await state.set_state(StartGenerationState.ask_video_length_input)


async def handle_ask_video_length_choice(
    call: types.CallbackQuery,
    state: FSMContext,
):
    choice = call.data.split("|")[1]
    state_data = await state.get_data()
    temp_path = state_data.get("temp_path_for_nsfw")
    prompt = state_data.get("prompt_for_nsfw_video")

    if choice == "default":
        await safe_edit_message(
            call.message,
            "⚙️ Генерация началась. Ожидайте...",
            reply_markup=None,
        )

        await generate_nsfw_video_and_send_result(
            call,
            state,
            prompt,
            temp_path,
            seconds=None,
        )
    elif choice == "input":
        input_msg = await safe_edit_message(
            call.message,
            "Введите желаемую длительность видео в секундах (максимум 15):",
        )
        await state.update_data(duration_prompt_msg_id=input_msg.message_id)
        await state.set_state(StartGenerationState.ask_video_length_input)


async def handle_ask_video_length_input(
    message: types.Message,
    state: FSMContext,
):
    try:
        await message.delete()
    except Exception as e:
        logger.warning(
            f"Не удалось удалить сообщение пользователя с длиной: {e}",
        )

    state_data = await state.get_data()
    duration_msg_id = state_data.get("duration_prompt_msg_id")
    if duration_msg_id:
        try:
            await bot.delete_message(message.chat.id, duration_msg_id)
        except Exception as e:
            logger.warning(
                f"Не удалось удалить сообщение бота с запросом длительности: {e}",
            )

    temp_path = state_data.get("temp_path_for_nsfw")
    prompt = state_data.get("prompt_for_nsfw_video")
    length = None
    try:
        if message.text and message.text.strip():
            length = int(message.text.strip())
            length = max(1, min(length, 15))
    except Exception:
        length = None

    await generate_nsfw_video_and_send_result(
        message,
        state,
        prompt,
        temp_path,
        seconds=length,
    )


# Обработка нажатия на кнопку сохранения видео
async def handle_video_save_button(
    call: types.CallbackQuery,
    state: FSMContext,
):
    # Получаем тип кнопки
    temp = call.data.split("|")
    model_name = temp[2]
    image_index = int(temp[3])
    video_index = int(temp[4])

    # Убираем кнопки у сообщения
    await call.message.edit_reply_markup(None)

    # Получаем данные
    state_data = await state.get_data()

    # Получаем путь к видео
    generated_nsfw_video_paths = state_data.get("generated_nsfw_video_paths", [])
    video_path = await getDataInDictsArray(
        generated_nsfw_video_paths,
        model_name,
        image_index,
        video_index,
    )

    if not video_path:
        error_message = "Ошибка: не удалось найти путь к видео для сохранения"
        await safe_send_message(
            error_message,
            call.message,
        )
        return None

    if image_index:
        # Удаляем изображение из массива объектов saved_images_urls
        saved_images_urls = state_data.get("saved_images_urls", [])
        for item in saved_images_urls:
            if model_name == item["model_name"] and image_index == item["image_index"] and video_index == item["video_index"]:
                saved_images_urls.remove(item)
        await state.update_data(saved_images_urls=saved_images_urls)

    # Сохраняем видео
    await saveVideo(video_path, model_name, call.message)


# Добавление обработчиков
def hand_add():
    router.callback_query.register(
        quick_generate_nsfw_video,
        lambda call: call.data.startswith("generate_comfyui_video"),
    )
    router.message.register(
        handle_prompt_for_nsfw_generation,
        StateFilter(StartGenerationState.write_prompt_for_nsfw_generation),
    )
    router.callback_query.register(
        handle_ask_video_length_choice,
        lambda call: call.data.startswith("video_length_choice|"),
        StateFilter(StartGenerationState.ask_video_length_input),
    )
    router.message.register(
        handle_ask_video_length_input,
        StateFilter(StartGenerationState.ask_video_length_input),
    )
