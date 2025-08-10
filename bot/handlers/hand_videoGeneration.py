import asyncio
import os

from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.helpers import text
from bot.helpers.generateImages.dataArray import (
    get_model_name_by_index,
)
from bot.helpers.handlers.messages import deleteMessageFromState
from bot.helpers.handlers.videoGeneration import (
    get_video_path_from_state,
    process_video,
    process_write_prompt,
    saveVideo,
)
from bot.app.instance import video_generation_router
from bot.app.core.logging import logger
from bot.app.config.settings import settings
from bot.states import StartGenerationState
from bot.utils.handlers import (
    getDataInDictsArray,
)
from bot.utils.handlers.getDataInDictsArray import getDataInDictsArray
from bot.utils.handlers.messages import (
    editMessageOrAnswer,
)
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)


# Обработка нажатия кнопки "⚡️Генерация видео с промптом"
async def quick_generate_video(call: types.CallbackQuery, state: FSMContext):
    temp = call.data.split("|")
    model_name = temp[1]

    if len(temp) == 3:
        image_index = int(temp[2])
        
        # Проверяем, есть ли сохраненные изображения для данной модели
        state_data = await state.get_data()
        saved_images_urls = state_data.get("saved_images_urls", [])
        model_entries = [entry for entry in saved_images_urls if entry.get("model_name") == model_name]
        
        # Проверяем, есть ли запись с указанным image_index
        matching_entry = next((entry for entry in model_entries if entry.get("image_index") == image_index), None)
        if not matching_entry:
            logger.warning(f"Запись для ({model_name}, {image_index}) не найдена в saved_images_urls. Доступные записи: {model_entries}")
            # Если нет записи с указанным image_index, используем первую доступную
            if model_entries:
                fallback_entry = model_entries[0]
                image_index = fallback_entry.get("image_index")
                logger.info(f"Используем fallback image_index {image_index} для модели {model_name}")

        await state.update_data(
            model_name_for_video_generation=model_name,
            image_index_for_video_generation=image_index,
        )
    else:
        image_index = None
        await state.update_data(
            model_name_for_video_generation=model_name,
        )

    # Получаем путь к видео (если он есть и это перегенерация)
    video_path = await get_video_path_from_state(state, model_name, image_index)

    # Удаляем видео из папки temp
    if not settings.MOCK_VIDEO_MODE and video_path:
        try:
            os.remove(video_path)
        except Exception as e:
            logger.error(f"Ошибка при удалении видео из папки temp: {e}")

    # Проверяем, добавилось ли имя модели в стейт
    state_data = await state.get_data()
    model_name_for_video_generation = state_data.get("model_name_for_video_generation", "")
    if model_name_for_video_generation != model_name:
        await state.update_data(model_name_for_video_generation=model_name)

    await process_write_prompt(
        call,
        state,
        model_name,
        image_index,
        is_quick_generation=True,
    )


async def handle_rewrite_prompt_button(
    call: types.CallbackQuery,
    state: FSMContext,
):
    _, model_name = call.data.split("|")

    state_data = await state.get_data()
    current_prompt = state_data.get("prompt_for_video", "")
    
    # Проверяем, есть ли сохраненные изображения для данной модели
    saved_images_urls = state_data.get("saved_images_urls", [])
    model_entries = [entry for entry in saved_images_urls if entry.get("model_name") == model_name]
    
    if not model_entries:
        logger.warning(f"Не найдено сохраненных изображений для модели {model_name}")
        await safe_send_message(
            f"Ошибка: не найдено сохраненных изображений для модели {model_name}",
            call.message,
        )
        return

    # Сохраняем model_name, чтобы потом знать куда применить
    await state.update_data(model_name_for_video_generation=model_name)

    # Обновляем сообщение
    await editMessageOrAnswer(
        call,
        f"✏️ Текущий промпт: {current_prompt}\n\nВведите новый промпт для генерации видео:",
        reply_markup=None,
    )

    # Проверяем, добавилось ли имя модели в стейт
    state_data = await state.get_data()
    model_name_for_video_generation = state_data.get("model_name_for_video_generation", "")
    if model_name_for_video_generation != model_name:
        await state.update_data(model_name_for_video_generation=model_name)

    # Ставим стейт для обработки ввода
    await state.set_state(StartGenerationState.write_prompt_for_quick_video_generation)


# Хедлер для обработки ввода кастомного промпта для видео
async def write_prompt_for_video(message: types.Message, state: FSMContext):
    # Получаем данные
    prompt = message.text
    await state.update_data(prompt_for_video=prompt)
    state_data = await state.get_data()

    model_name = state_data.get("model_name_for_video_generation", "")
    image_index = state_data.get("image_index_for_video_generation", None)

    if image_index:
        image_index = int(image_index)
        saved_images_urls = state_data.get("saved_images_urls", [])

        logger.info(
            f"Произвожу поиск изображения по индексу {image_index} и имени модели {model_name} в массиве: {saved_images_urls}",
        )

        # Проверяем, есть ли записи для данной модели
        model_entries = [entry for entry in saved_images_urls if entry.get("model_name") == model_name]
        logger.info(f"Найдено записей для модели {model_name}: {model_entries}")
        
        # Проверяем, есть ли запись с нужным image_index
        matching_entry = next((entry for entry in model_entries if entry.get("image_index") == image_index), None)
        if matching_entry:
            logger.info(f"Найдена запись для ({model_name}, {image_index}): {matching_entry}")
        else:
            logger.warning(f"Запись для ({model_name}, {image_index}) не найдена. Доступные записи для модели: {model_entries}")

        image_url = await getDataInDictsArray(
            saved_images_urls,
            model_name,
            image_index,
        )

        if not image_url:
            # Пытаемся найти любую запись для данной модели
            fallback_entry = next((entry for entry in model_entries if entry.get("direct_url")), None)
            if fallback_entry:
                logger.warning(f"Используем fallback запись для модели {model_name}: {fallback_entry}")
                image_url = fallback_entry.get("direct_url")
                # Обновляем image_index на найденный
                image_index = fallback_entry.get("image_index")
                await state.update_data(image_index_for_video_generation=image_index)
            else:
                error_message = f"Ошибка: не удалось найти URL изображения для модели {model_name} с индексом {image_index}. Доступные записи: {model_entries}"
                logger.error(error_message)
                raise Exception(error_message)

    else:
        # Сначала проверяем данные из режима уникальных промптов
        img2video_data = state_data.get("img2video_data", [])
        temp_path = None
        
        if img2video_data:
            # Ищем путь к изображению для данной модели
            for data in img2video_data:
                if get_model_name_by_index(data['model_index']) == model_name:
                    # Получаем путь к изображению из temp_paths_for_video_generation по индексу
                    temp_paths_for_video_generation = state_data.get("temp_paths_for_video_generation", [])
                    if data['image_index'] <= len(temp_paths_for_video_generation):
                        temp_path = temp_paths_for_video_generation[data['image_index'] - 1]
                    break
        
        # Если не найдено в img2video_data, ищем в старом формате
        if not temp_path:
            img2video_temp_paths_for_with_model_names = state_data.get(
                "img2video_temp_paths_for_with_model_names", {}
            )
            temp_path = img2video_temp_paths_for_with_model_names.get(model_name, None)

        if not temp_path:
            await safe_send_message(
                "Ошибка: не удалось найти путь к изображению",
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

    await state.set_state(None)

    if image_index:
        logger.info(
            f"URL изображения для генерации видео модели {model_name}: {image_url}",
        )

        # сразу генерируем видео
        return await process_video(
            state=state,
            model_name=model_name,
            prompt=prompt,
            image_url=image_url,
            image_index=image_index,
            message=message,
        )
    else:
        logger.info(
            f"Путь изображения для генерации видео модели {model_name}: {temp_path}",
        )

        # сразу генерируем видео
        return await process_video(
            state=state,
            model_name=model_name,
            prompt=prompt,
            image_path=temp_path,
            message=message,
        )


# Обработка нажатия на кнопку сохранения видео
async def handle_video_save_button(
    call: types.CallbackQuery,
    state: FSMContext,
):
    # Получаем тип кнопки
    temp = call.data.split("|")
    model_name = temp[2]

    if len(temp) == 4:
        image_index = int(temp[3])
    else:
        image_index = None

    # Убираем кнопки у сообщения
    await call.message.edit_reply_markup(None)

    # Получаем данные
    state_data = await state.get_data()

    # Получаем путь к видео
    video_path = await get_video_path_from_state(state, model_name, image_index)

    if not video_path:
        error_message = "Ошибка: не удалось найти путь к видео для сохранения"
        await safe_send_message(
            error_message,
            call.message,
        )
        return None

    # Сохраняем видео
    await saveVideo(video_path=video_path, model_name=model_name, message=call.message)

    if image_index:
        # Удаляем сообщение о генерации видео
        await deleteMessageFromState(
            state,
            "videoGeneration_messages_ids",
            model_name,
            call.message.chat.id,
            image_index=image_index,
        )


# Обработка нажатия на кнопку "✨ Сгенерировать все видео по 1 промпту"
async def handle_generate_video_by_one_prompt(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text.WRITE_PROMPT_FOR_VIDEO_GENERATION_BY_ONE_PROMPT_TEXT,
        reply_markup=None,
    )

    await state.set_state(StartGenerationState.write_prompt_for_video_generation_by_one_prompt)


# Обработка ввода промпта на генерацию видео по 1 промпту
async def write_prompt_for_video_generation_by_one_prompt(message: types.Message, state: FSMContext):
    prompt = message.text
    await state.update_data(prompt_for_video_generation_by_one_prompt=prompt)

    await state.set_state(None)

    state_data = await state.get_data()
    saved_images_urls = state_data.get("saved_images_urls", [])

    tasks = []
    for obj in saved_images_urls:
        task = asyncio.create_task(
            process_video(
                state=state,
                model_name=obj["model_name"],
                prompt=prompt,
                image_url=obj["direct_url"],
                image_index=obj["image_index"],
                message=message,
            ),
        )
        tasks.append(task)

        # Удаляем сообщение с изображением
        await deleteMessageFromState(
            state,
            "messages_with_saved_images",
            obj["model_name"],
            message.chat.id,
            image_index=obj["image_index"],
        )
        await asyncio.sleep(0.5)

    # Если нужно дождаться завершения всех задач:
    await asyncio.gather(*tasks)


# Добавление обработчиков
def hand_add():
    video_generation_router.callback_query.register(
        quick_generate_video,
        lambda call: call.data.startswith("quick_video_generation"),
    )

    video_generation_router.callback_query.register(
        handle_rewrite_prompt_button,
        lambda call: call.data.startswith("rewrite_prompt|"),
    )
    video_generation_router.message.register(
        write_prompt_for_video,
        StateFilter(
            StartGenerationState.write_prompt_for_video,
            StartGenerationState.write_prompt_for_quick_video_generation,
        ),
    )

    video_generation_router.callback_query.register(
        handle_video_save_button,
        lambda call: call.data.startswith("video_correctness|correct"),
    )

    video_generation_router.callback_query.register(
        handle_generate_video_by_one_prompt,
        lambda call: call.data.startswith("generate_video_by_one_prompt"),
    )

    video_generation_router.message.register(
        write_prompt_for_video_generation_by_one_prompt,
        StateFilter(StartGenerationState.write_prompt_for_video_generation_by_one_prompt),
    )