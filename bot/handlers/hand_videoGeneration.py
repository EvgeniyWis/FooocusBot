from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.helpers.handlers.messages import deleteMessageFromState
from bot.helpers.handlers.videoGeneration import (
    process_video,
    process_write_prompt,
    saveVideo,
)
from bot.InstanceBot import router
from bot.logger import logger
from bot.states import StartGenerationState
from bot.utils.handlers import (
    getDataInDictsArray,
)
from bot.utils.handlers.messages import (
    editMessageOrAnswer,
)
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)


# Обработка нажатия кнопки "⚡️Генерация видео с промптом"
async def quick_generate_video(call: types.CallbackQuery, state: FSMContext):
    model_name = call.data.split("|")[1]
    image_index = call.data.split("|")[2]

    state_data = await state.get_data()

    await state.update_data(
        model_name_for_video_generation=model_name,
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
    await state.set_state(StartGenerationState.write_prompt_for_quick_video_generation)


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

    logger.info(
        f"URL изображения для генерации видео модели {model_name}: {image_url}",
    )

    await state.set_state(None)

    # сразу генерируем видео
    return await process_video(
        state=state,
        model_name=model_name,
        prompt=prompt,
        type_for_video_generation="work",
        image_url=image_url,
        image_index=image_index,
        message=message,
    )


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
