import asyncio
import os
import traceback

from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

import bot.constants as constants
from bot.factory.comfyui_video_service import get_video_service
from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    getModelNameIndex,
)
from bot.helpers.generateImages.dataArray.getModelNameByIndex import (
    getModelNameByIndex,
)
from bot.helpers.handlers.messages import deleteMessageFromState
from bot.helpers.handlers.videoGeneration import (
    check_video_path,
    process_video,
    process_write_prompt,
    saveVideo,
)
from bot.InstanceBot import bot, router
from bot.keyboards import video_generation_keyboards
from bot.logger import logger
from bot.states import StartGenerationState
from bot.utils import retryOperation
from bot.utils.handlers import (
    getDataInDictsArray,
)
from bot.utils.handlers.messages import (
    editMessageOrAnswer,
)
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)
from bot.utils.handlers.messages.rate_limiter_for_send_photo import (
    safe_send_photo,
)
from bot.utils.videos.download_nsfw_video import (
    download_nsfw_videos,
)
from bot.utils.videos.generate_nsfw_video import generate_nsfw_video


# Обработка нажатия кнопки "⚡️Генерация видео с промптом"
async def quick_generate_video(call: types.CallbackQuery, state: FSMContext):
    model_name = call.data.split("|")[1]
    image_index = call.data.split("|")[2]

    if not call.message.photo:
        await call.answer("Ошибка: не найдено изображение в сообщении")
        return

    photo = call.message.photo[-1]
    file_id = photo.file_id

    state_data = await state.get_data()

    await state.update_data(
        model_name_for_video_generation=model_name,
        image_file_id_for_videoGenerationFromImage=file_id,
        image_index_for_video_generation=image_index,
        saved_images_urls=state_data.get("saved_images_urls", []),
    )

    await process_write_prompt(
        call,
        state,
        model_name,
        is_quick_generation=True,
    )


async def handle_rewrite_prompt_button(
    call: types.CallbackQuery,
    state: FSMContext,
):
    _, model_name = call.data.split("|")

    state_data = await state.get_data()
    current_prompt = state_data.get("prompt_for_video", "")

    # Обновляем сообщение
    await editMessageOrAnswer(
        call,
        f"✏️ Текущий промпт: {current_prompt}\n\nВведите новый промпт для генерации видео:",
        reply_markup=None,
    )

    # Сохраняем model_name, чтобы потом знать куда применить
    await state.update_data(model_name_for_video_generation=model_name)

    # Ставим стейт для обработки ввода
    await state.set_state(StartGenerationState.write_prompt_for_video)


# Обработка нажатия кнопок режима генерации видео
async def handle_video_generation_mode_buttons(
    call: types.CallbackQuery,
    state: FSMContext,
):
    # Получаем индекс модели
    temp = call.data.split("|")
    model_name = temp[1]

    # Получаем выбранный режим генерации видео
    mode = temp[2]

    # Если выбран режим "Написать свой промпт", то отправляем сообщение для ввода кастомного промпта
    if mode == "write_prompt":
        await process_write_prompt(
            call,
            state,
            model_name,
        )
        return

    # TODO: режим генерации видео с видео-примерами временно отключен
    # Если выбран режим "Использовать заготовленные примеры", то отправляем сообщение с видео-примерами
    # elif mode == "use_examples":
    #     # Получаем все видео-шаблоны с их промптами
    #     templates_examples = await getVideoExamplesData()

    #     # Выгружаем видео-примеры вместе с их промптами
    #     video_examples_messages_ids = []
    #     for index, value in templates_examples.items():
    #         video_example_message = await call.message.answer_video(
    #             video=value["file_id"],
    #             caption=text.VIDEO_EXAMPLE_TEXT.format(model_name, model_name_index, value["prompt"]),
    #             reply_markup=video_generation_keyboards.generatedVideoKeyboard(f"generate_video|{index}|{model_name}")
    #         )
    #         video_examples_messages_ids.append(video_example_message.message_id)
    #         await state.update_data(video_examples_messages_ids=video_examples_messages_ids)


# Обработка нажатия кнопок под видео-примером
async def handle_video_example_buttons(
    call: types.CallbackQuery,
    state: FSMContext,
):
    # Удаляем текущее сообщение
    try:
        await call.message.delete()
    except Exception as e:
        logger.error(f"Произошла ошибка при удалении сообщения: {e}")

    # Получаем индекс видео-примера и тип кнопки
    temp = call.data.split("|")

    if len(temp) == 4:
        # TODO: режим генерации видео с видео-примерами временно отключен
        # index = int(temp[1])
        model_name = temp[2]
        image_index = int(temp[3])
        type_for_video_generation = temp[3]
        # await state.update_data(video_example_index=index)
    else:
        model_name = temp[1]
        image_index = int(temp[2])
        type_for_video_generation = temp[3]

    # Получаем название модели и url изображения
    state_data = await state.get_data()
    saved_images_urls = state_data.get("saved_images_urls", [])
    image_url = await getDataInDictsArray(saved_images_urls, model_name, image_index)

    # Удаляем сообщение с выбором видео-примера
    # TODO: режим генерации видео с видео-примерами временно отключен
    # try:
    #     await bot.delete_message(user_id, int(data["select_video_example_message_id"]))
    # except Exception as e:
    #     logger.error(f"Произошла ошибка при удалении сообщения с id {data['select_video_example_message_id']}: {e}")

    # if len(temp) == 4:
    #     # Получаем данные видео-примера по его индексу
    #     video_example_data = await getVideoExampleDataByIndex(index)

    # Получаем кастомный промпт, если он есть, а если нет, то берем промпт из видео-примера
    if "prompt_for_video" in state_data:
        custom_prompt = state_data.get("prompt_for_video", "")
        await state.update_data(prompt_for_video=custom_prompt)
    else:
        custom_prompt = None

    # TODO: режим генерации видео с видео-примерами временно отключен, поэтому кастомный промпт используется
    video_example_prompt = custom_prompt

    # TODO: режим генерации видео с видео-примерами временно отключен
    # if custom_prompt:
    #     video_example_prompt = custom_prompt
    # else:
    #     video_example_prompt = video_example_data["prompt"]

    # # Удаляем сообщения с видео-примерами
    # if "video_examples_messages_ids" in data:
    #     video_examples_messages_ids = data["video_examples_messages_ids"]

    #     for message_id in video_examples_messages_ids:
    #         try:
    #             await bot.delete_message(user_id, int(message_id))
    #         except Exception as e:
    #             logger.error(f"Произошла ошибка при удалении сообщения с id {message_id}: {e}")

    await process_video(
        state=state,
        model_name=model_name,
        prompt=video_example_prompt,
        type_for_video_generation=type_for_video_generation,
        image_url=image_url,
        image_index=image_index,
        call=call,
    )


# Хедлер для обработки ввода кастомного промпта для видео
async def write_prompt_for_video(message: types.Message, state: FSMContext):
    # Получаем данные
    prompt = message.text
    await state.update_data(prompt_for_video=prompt)
    state_data = await state.get_data()
    model_name = state_data.get("model_name_for_video_generation", "")
    image_index = int(state_data.get("image_index_for_video_generation", 0))
    saved_images_urls = state_data.get("saved_images_urls", [])

    logger.info(
        f"Произвожу поиск изображения по индексу {image_index} и имени модели {model_name} в массиве: {saved_images_urls}",
    )

    image_url = await getDataInDictsArray(
        saved_images_urls,
        model_name,
        image_index,
    )

    if not image_url:
        await safe_send_message(
            "Ошибка: не удалось найти URL изображения",
            message,
        )
        return

    # Удаляем сообщение пользователя
    await message.delete()

    # Удаляем сообщение о написании промпта
    await deleteMessageFromState(
        state,
        "write_prompt_messages_ids",
        model_name,
        message.chat.id,
        image_index=image_index,
    )

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    logger.info(
        f"URL изображения для генерации видео модели {model_name}: {image_url}",
    )

    current_state = await state.get_state()

    # Если выбрана быстрая генерация видео, то сразу генерируем видео
    if (
        current_state
        == StartGenerationState.write_prompt_for_quick_video_generation
    ):
        return await process_video(
            state=state,
            model_name=model_name,
            prompt=prompt,
            type_for_video_generation="work",
            image_url=image_url,
            image_index=image_index,
            message=message,
        )
    else:
        # Если выбрана простая генерация видео, то сначала отправляем фото, а потом генерируем видео
        try:
            await safe_send_photo(
                photo=image_url,
                message=message,
                caption=text.WRITE_PROMPT_FOR_VIDEO_SUCCESS_TEXT.format(
                    model_name,
                    model_name_index,
                ),
                reply_markup=video_generation_keyboards.videoGenerationTypeKeyboard(
                    model_name,
                    image_index,
                    True,
                ),
            )
        except Exception as e:
            # Если не удалось отправить фото, отправляем только текст
            await safe_send_message(
                text.WRITE_PROMPT_FOR_VIDEO_SUCCESS_TEXT.format(
                    model_name,
                    model_name_index,
                ),
                message,
                reply_markup=video_generation_keyboards.videoGenerationTypeKeyboard(
                    model_name,
                    image_index,
                    True,
                ),
            )

            raise e

    await state.set_state(None)


# Обработка нажатия на кнопки корректности видео
async def handle_video_correctness_buttons(
    call: types.CallbackQuery,
    state: FSMContext,
):
    # Получаем тип кнопки
    temp = call.data.split("|")
    model_name = temp[2]
    image_index = int(temp[3])

    # Убираем кнопки у сообщения
    await call.message.edit_reply_markup(None)

    # Получаем данные
    state_data = await state.get_data()

    # Получаем путь к видео
    generated_video_paths = state_data.get("generated_video_paths", [])
    logger.info(
        f"Получены пути к видео: {generated_video_paths} и попытка получить путь к видео по имени модели {model_name} и индексу изображения {image_index}",
    )
    video_path = await getDataInDictsArray(
        generated_video_paths,
        model_name,
        image_index,
    )

    if not video_path:
        await safe_send_message(
            "Ошибка: не удалось найти путь к видео для сохранения",
            call.message,
        )
        return

    logger.info(f"Получен путь к видео для сохранения: {video_path}")

    # Удаляем изображение из массива объектов saved_images_urls
    saved_images_urls = state_data.get("saved_images_urls", [])
    for item in saved_images_urls:
        if model_name in item.keys():
            saved_images_urls.remove(item)
    await state.update_data(saved_images_urls=saved_images_urls)

    # Сохраняем видео
    await saveVideo(video_path, model_name, call.message)

    # Удаляем сообщение о генерации видео
    await deleteMessageFromState(
        state,
        "videoGeneration_messages_ids",
        model_name,
        call.message.chat.id,
        image_index=image_index,
    )


# Обработка нажатия на кнопку "📹 Сгенерировать видео из изображения'"
async def start_generateVideoFromImage(
    call: types.CallbackQuery,
    state: FSMContext,
):
    await call.message.edit_text(text.SEND_IMAGE_FOR_VIDEO_GENERATION)
    await state.set_state(StartGenerationState.send_image_for_video_generation)

    # Очищаем стейт от всех данных
    # TODO: убрать и сделать так, чтобы можно было генерить одновременно несколько видео
    # await state.update_data(image_file_ids_for_videoGenerationFromImage=[])
    # await state.update_data(prompts_for_videoGenerationFromImage={})
    # await state.update_data(generated_video_paths=[])


# Обработка присылания изображения для генерации видео и запроса на присылания промпта
async def write_prompt_for_videoGenerationFromImage(
    message: types.Message,
    state: FSMContext,
):
    # Проверяем, есть ли изображение в сообщении
    if not message.photo:
        await safe_send_message(
            text.NO_IMAGE_FOR_VIDEO_GENERATION_ERROR_TEXT,
            message,
        )
        return

    # Получаем file_id самого большого изображения
    photo = message.photo[-1]
    await state.update_data(
        image_file_id_for_videoGenerationFromImage=photo.file_id,
    )

    # Просим пользователя ввести промпт для генерации видео
    await state.set_state(None)
    await safe_send_message(
        text.WRITE_PROMPT_FOR_VIDEO_GENERATION_FOR_IMAGE_TEXT,
        message,
    )
    await state.set_state(
        StartGenerationState.write_prompt_for_videoGenerationFromImage,
    )


# Хендлер для обработки промпта для генерации видео из изображения
async def handle_prompt_for_videoGenerationFromImage(
    message: types.Message,
    state: FSMContext,
):
    # Получаем промпт
    prompt = message.text

    await state.update_data(prompt_for_videoGenerationFromImage=prompt)
    state_data = await state.get_data()
    image_file_id = state_data.get(
        "image_file_id_for_videoGenerationFromImage",
    )

    if not image_file_id:
        await safe_send_message(
            text.NO_IMAGE_FOR_VIDEO_GENERATION_ERROR_TEXT,
            message,
        )
        return

    # Отправляем сообщение о прогрессе
    generate_video_from_image_progress_message = await safe_send_message(
        text.GENERATE_VIDEO_FROM_IMAGE_PROGRESS_TEXT,
        message,
    )

    try:
        # Скачиваем изображение (file_id) и получаем путь к файлу
        # Для этого используем bot.download_file и сохраняем во временную папку
        try:
            file = await asyncio.wait_for(
                bot.get_file(image_file_id),
                timeout=30,
            )
        except TimeoutError:
            await safe_send_message(
                "⏰ Время ожидания получения файла Telegram истекло. Попробуйте позже.",
                message,
            )
            raise TimeoutError(
                "Время ожидания получения файла Telegram истекло.",
            )

        file_path = file.file_path
        temp_path = f"{constants.TEMP_IMAGE_FILES_DIR}/{image_file_id}.jpg"

        try:
            await asyncio.wait_for(
                bot.download_file(file_path, temp_path),
                timeout=60,
            )
        except TimeoutError:
            await safe_send_message(
                "⏰ Время ожидания скачивания файла Telegram истекло. Попробуйте позже.",
                message,
            )
            raise TimeoutError(
                "Время ожидания скачивания файла Telegram истекло.",
            )

        # Генерируем видео
        video_path = await check_video_path(
            prompt,
            message,
            image_index=None,
            image_url=None,
            temp_path=temp_path,
            model_name=None,
        )

        await generate_video_from_image_progress_message.delete()

        if not video_path:
            return

        await state.update_data(
            video_path=video_path,
        )

        video = types.FSInputFile(video_path)
        await message.answer_video(
            video=video,
            caption=text.GENERATE_VIDEO_FROM_IMAGE_SUCCESS_TEXT,
        )

        # Спрашиваем, в папку какой модели сохранить видео
        await state.set_state(None)
        await safe_send_message(
            text.ASK_FOR_MODEL_NAME_FOR_VIDEO_GENERATION_FROM_IMAGE_TEXT,
            message,
        )
        await state.set_state(
            StartGenerationState.ask_for_model_name_for_video_generation_from_image,
        )

        # Удаляем временное изображение
        os.remove(temp_path)
    except Exception as e:
        traceback.print_exc()
        raise e


# Хендлер для обработки ввода имени модели для сохранения видео
async def handle_model_name_for_video_generation_from_image(
    message: types.Message,
    state: FSMContext,
):
    # Получаем данные
    state_data = await state.get_data()
    # file_id_index = int(state_data.get("current_file_id_index", 0))

    # Получаем данные по имени модели
    try:
        model_index = int(message.text)
    except Exception as e:
        logger.error(f"Произошла ошибка при получении индекса модели: {e}")
        await safe_send_message(
            text.WRONG_MODEL_INDEX_TEXT.format(message.text),
            message,
        )
        return

    # Если индекс больше 100 или меньше 1, то просим ввести другой индекс
    if model_index > 100 or model_index < 1:
        await safe_send_message(
            text.MODEL_NOT_FOUND_TEXT.format(model_index),
            message,
        )
        return

    # Получаем путь к видео
    # logger.info(f"Попытка получить путь к видео: {state_data.get('generated_video_paths', [])} по индексу: {file_id_index}")
    # video_path = state_data.get("generated_video_paths", [])[file_id_index]
    video_path = state_data.get("video_path", "")

    # Получаем название модели по индексу
    model_name = getModelNameByIndex(model_index)

    # Сохраняем видео
    await state.set_state(None)
    await saveVideo(video_path, model_name, message)

    # TODO: вернуть
    # try:
    #     # Очищаем все стейты от текущих данных
    #     await state.update_data(current_file_id_index=None)

    #     # Получаем file_id изображения, которое нужно удалить
    #     image_file_id = state_data.get("image_file_ids_for_videoGenerationFromImage", [])[file_id_index]
    #     # Удаляем видео из списка и обновляем state
    #     updated_generated_video_paths = state_data.get("generated_video_paths", [])
    #     updated_generated_video_paths.pop(file_id_index)
    #     await state.update_data(generated_video_paths=updated_generated_video_paths)

    #     # Удаляем file_id из списка и обновляем state
    #     updated_image_file_ids = state_data.get("image_file_ids_for_videoGenerationFromImage", [])
    #     updated_image_file_ids.pop(file_id_index)
    #     await state.update_data(image_file_ids_for_videoGenerationFromImage=updated_image_file_ids)

    #     # Удаляем промпт по file_id и обновляем state
    #     updated_prompts = state_data.get("prompts_for_videoGenerationFromImage", {})
    #     updated_prompts.pop(image_file_id)
    #     await state.update_data(prompts_for_videoGenerationFromImage=updated_prompts)
    #     logger.info(f"Удалены данные из массивов: {updated_generated_video_paths}, {updated_image_file_ids}, {updated_prompts}")
    # except Exception as e:
    #     logger.error(f"Произошла ошибка при сохранении видео: {e}")


async def quick_generate_nsfw_video(
    call: types.CallbackQuery,
    state: FSMContext,
):
    model_name = call.data.split("|")[1]

    if not call.message.photo:
        logger.error(f"Для {model_name} не нашлось изображение в сообщении")
        await call.answer("Ошибка: не найдено изображение в сообщении")
        return

    photo = call.message.photo[-1]
    file_id = photo.file_id

    state_data = await state.get_data()

    await state.update_data(
        model_name_for_nsfw_video_generation=model_name,
        image_file_id_for_nsfw_videoGenerationFromImage=file_id,
        saved_images_urls=state_data.get("saved_images_urls", []),
    )

    await process_write_prompt(
        call,
        state,
        model_name,
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
    try:
        result_final = await video_service.wait_for_result(
            prompt_id,
        )
    except Exception:
        try:
            await retryOperation(
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

    await progress_message.delete()

    if result_final.get("video_urls"):
        video_urls = result_final["video_urls"]
        await state.update_data(generated_nsfw_video_urls=video_urls)

        async for v in download_nsfw_videos(video_urls):
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
            )(video=video, caption=v.caption)

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
    state_data = await state.get_data()
    file_id = state_data.get("image_file_id_for_nsfw_videoGenerationFromImage")

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
    await safe_send_message(
        "⏳ Выберите способ задания длительности видео:",
        message,
        reply_markup=video_generation_keyboards.nsfw_video_generation_insert_length_video_keyboard(),
    )
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
        await generate_nsfw_video_and_send_result(
            call,
            state,
            prompt,
            temp_path,
            seconds=None,
        )
    elif choice == "input":
        await safe_send_message(
            "Введите желаемую длительность видео в секундах (максимум 15):",
            call,
        )
        await state.set_state(StartGenerationState.ask_video_length_input)


async def handle_ask_video_length_input(
    message: types.Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    temp_path = state_data.get("temp_path_for_nsfw")
    prompt = state_data.get("prompt_for_nsfw_video")
    length = None
    try:
        if message.text and message.text.strip():
            length = int(message.text.strip())
            if length > 15:
                length = 15
            if length < 1:
                length = 5
    except Exception:
        length = None
    await generate_nsfw_video_and_send_result(
        message,
        state,
        prompt,
        temp_path,
        seconds=length,
    )


# Добавление обработчиков
def hand_add():
    router.callback_query.register(
        quick_generate_video,
        lambda call: call.data.startswith("quick_video_generation"),
    )

    router.callback_query.register(
        handle_video_generation_mode_buttons,
        lambda call: call.data.startswith("generate_video_mode"),
    )

    router.callback_query.register(
        handle_video_example_buttons,
        lambda call: call.data.startswith("generate_video"),
    )
    router.callback_query.register(
        handle_rewrite_prompt_button,
        lambda call: call.data.startswith("rewrite_prompt|"),
    )
    router.message.register(
        write_prompt_for_video,
        StateFilter(
            StartGenerationState.write_prompt_for_video,
            StartGenerationState.write_prompt_for_quick_video_generation,
        ),
    )

    router.callback_query.register(
        handle_video_correctness_buttons,
        lambda call: call.data.startswith("video_correctness"),
    )

    router.callback_query.register(
        start_generateVideoFromImage,
        lambda call: call.data == "generateVideoFromImage",
    )

    router.message.register(
        write_prompt_for_videoGenerationFromImage,
        StateFilter(StartGenerationState.send_image_for_video_generation),
    )

    router.message.register(
        handle_prompt_for_videoGenerationFromImage,
        StateFilter(
            StartGenerationState.write_prompt_for_videoGenerationFromImage,
        ),
    )

    router.message.register(
        handle_model_name_for_video_generation_from_image,
        StateFilter(
            StartGenerationState.ask_for_model_name_for_video_generation_from_image,
        ),
    )

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
