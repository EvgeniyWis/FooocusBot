import asyncio
import os
import shutil

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.constants import MULTI_IMAGE_NUMBER, TEMP_FOLDER_PATH
from bot.helpers.handlers.messages import deleteMessageFromState
from bot.helpers.handlers.startGeneration import (
    process_image,
)
from bot.InstanceBot import router
from bot.logger import logger


async def select_multi_image(
    call: types.CallbackQuery,
    state: FSMContext,
):
    _, model_name, setting_number, image_index = call.data.split("|")
    image_index = int(image_index)
    message_id = call.message.message_id
    state_data = await state.get_data()
    mediagroup_data = state_data.get(
        "imageGeneration_mediagroup_messages_ids",
        [],
    )

    generation_id = None

    # Ищем generation_id по текущему message_id и type='keyboard'
    for item in mediagroup_data:
        if (
            item.get("type") == "keyboard"
            and item.get("message_id") == message_id
        ):
            generation_id = item.get("generation_id")
            break

    if not generation_id:
        logger.exception(
            f"[select_multi_image] generation_id not found for message_id={message_id} in state_data={state_data}",
        )
        raise Exception("generation_id is None")

    selected_indexes_raw = state_data.get("selected_indexes", {})
    if isinstance(selected_indexes_raw, list):
        selected_indexes_dict = {generation_id: selected_indexes_raw}
    else:
        selected_indexes_dict = selected_indexes_raw
    selected_indexes = selected_indexes_dict.get(generation_id, [])

    if image_index in selected_indexes:
        selected_indexes.remove(image_index)
    else:
        if len(selected_indexes) < MULTI_IMAGE_NUMBER:
            selected_indexes.append(image_index)

    selected_indexes_dict[generation_id] = selected_indexes
    await state.update_data(selected_indexes=selected_indexes_dict)

    from bot.keyboards.startGeneration.keyboards import (
        selectMultiImageKeyboard,
    )

    kb = selectMultiImageKeyboard(
        model_name,
        setting_number,
        MULTI_IMAGE_NUMBER,
        selected_indexes,
        generation_id,
    )
    await call.message.edit_reply_markup(reply_markup=kb)
    await call.answer()


async def multi_image_done(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    _, model_name, setting_number, generation_id = call.data.split("|")

    selected_indexes_raw = state_data.get("selected_indexes", {})
    if isinstance(selected_indexes_raw, list):
        selected_indexes_dict = {generation_id: selected_indexes_raw}
    else:
        selected_indexes_dict = selected_indexes_raw
    full_generation_id = next(
        (
            k
            for k in selected_indexes_dict.keys()
            if k.startswith(generation_id)
        ),
        None,
    )
    selected_indexes = selected_indexes_dict.get(full_generation_id, [])

    if not selected_indexes:
        await call.answer(
            "Выберите хотя бы одно изображение!",
            show_alert=True,
        )
        return

    temp_dir = TEMP_FOLDER_PATH / f"{model_name}_{call.from_user.id}"
    if os.path.exists(temp_dir):
        files_in_dir = sorted(os.listdir(temp_dir))
        logger.info(
            f"[multi_image_done] Существующие файлы в {temp_dir}: {files_in_dir}",
        )
        # Фильтруем selected_indexes по реально существующим файлам
        existing_indexes = set()
        for fname in files_in_dir:
            if fname.endswith(".jpg") and fname[:-4].isdigit():
                existing_indexes.add(int(fname[:-4]))
        filtered_selected_indexes = [
            i for i in selected_indexes if i in existing_indexes
        ]
        skipped_indexes = [
            i for i in selected_indexes if i not in existing_indexes
        ]
        if skipped_indexes:
            logger.warning(
                f"[multi_image_done] Эти индексы выбраны пользователем, но файлов нет: {skipped_indexes}",
            )
        selected_indexes = filtered_selected_indexes
    else:
        logger.warning(f"[multi_image_done] Директория {temp_dir} не найдена!")
    logger.info(
        f"[multi_image_done] RAW selected_indexes: {selected_indexes}",
    )
    selected_indexes_sorted = sorted(selected_indexes)
    logger.info(
        f"[multi_image_done] SORTED selected_indexes: {selected_indexes_sorted}",
    )

    await deleteMessageFromState(
        state,
        "imageGeneration_mediagroup_messages_ids",
        model_name,
        call.message.chat.id,
        delete_keyboard_message=True,
        generation_id=generation_id,
    )

    tasks = []

    for idx, image_index in enumerate(selected_indexes_sorted, 1):
        logger.info(
            f"[multi_image_done] Обрабатываю image_index={image_index}",
        )

        status_message = await call.message.answer(
            f"🔄 Работаю с изображением для модели {model_name} под номером {image_index}... (обработано {idx}/{len(selected_indexes_sorted)})",
        )

        # Создаём фейковый call для каждой задачи
        fake_call = types.CallbackQuery(
            id=call.id,
            from_user=call.from_user,
            chat_instance=call.chat_instance,
            message=status_message,
            data=call.data,
            inline_message_id=call.inline_message_id,
        )

        task = asyncio.create_task(
            process_image(fake_call, state, model_name, image_index),
        )
        tasks.append(task)

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for index, result in enumerate(results):
        if isinstance(result, Exception):
            image_index = selected_indexes_sorted[index]
            logger.error(
                f"Ошибка при обработке изображения {image_index}: {result}",
            )
            await call.message.answer(
                f"❌ Ошибка при обработке изображения {image_index}: {str(result)}",
            )

    await call.message.answer(
        f"✅ Все выбранные изображения для модели {model_name} успешно обработаны!",
    )

    # Удаляем папку модели с оставшимися изображениями
    try:
        temp_path = os.path.join(
            TEMP_FOLDER_PATH,
            f"{model_name}_{call.from_user.id}",
        )
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
    except Exception as e:
        logger.error(f"Ошибка при удалении папки модели {model_name}: {e}")


# Добавление обработчиков
def hand_add():
    router.callback_query.register(
        select_multi_image,
        lambda call: call.data.startswith("select_multi_image"),
    )

    router.callback_query.register(
        multi_image_done,
        lambda call: call.data.startswith("multi_image_done"),
    )
