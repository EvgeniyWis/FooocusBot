import asyncio
import os
import shutil

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.constants import (
    FACEFUSION_TEMP_IMAGES_FOLDER_PATH,
    MULTI_IMAGE_NUMBER,
)
from bot.helpers.handlers.messages import deleteMessageFromState
from bot.helpers.handlers.startGeneration import (
    process_image,
)
from bot.helpers.handlers.startGeneration.resolve_job_id import resolve_job_id
from bot.InstanceBot import multi_image_router
from bot.logger import logger


async def select_multi_image(
    call: types.CallbackQuery,
    state: FSMContext,
):
    parts = call.data.split("|")
    # поддержка старого формата без short_job_id и нового с ним
    if len(parts) == 5:
        _, full_model_key, group_number, image_index, short_job_id = parts
    else:
        _, full_model_key, group_number, image_index = parts
        short_job_id = None
    
    # Извлекаем model_name и model_key из полного ключа
    if "_" in full_model_key:
        model_name, model_key = full_model_key.rsplit("_", 1)
    else:
        model_name = full_model_key
        model_key = None
    
    image_index = int(image_index)
    message_id = call.message.message_id
    state_data = await state.get_data()

    # Используем хелпер для определения job_id
    job_id = resolve_job_id(
        state_data=state_data,
        model_name=model_name,
        model_key=model_key,
        message_id=message_id,
        short_job_id=short_job_id,
    )

    if not job_id:
        target_full_key = f"{model_name}_{model_key}" if model_key is not None else model_name
        logger.exception(
            f"[select_multi_image] job_id not found for message_id={message_id}, model_name={model_name}, short={short_job_id}, full_model_key={target_full_key} in state_data={state_data}",
        )
        # текущее поведение — кидаем исключение
        raise RuntimeError("Не удалось определить задание. Попробуйте снова отправить генерацию.")

    selected_indexes_raw = state_data.get("selected_indexes", {})
    if isinstance(selected_indexes_raw, list):
        selected_indexes_dict = {job_id: selected_indexes_raw}
    else:
        selected_indexes_dict = selected_indexes_raw
    selected_indexes = selected_indexes_dict.get(job_id, [])

    if image_index in selected_indexes:
        selected_indexes.remove(image_index)
    else:
        if len(selected_indexes) < MULTI_IMAGE_NUMBER:
            selected_indexes.append(image_index)

    selected_indexes_dict[job_id] = selected_indexes
    await state.update_data(selected_indexes=selected_indexes_dict)

    from bot.keyboards.startGeneration.keyboards import (
        selectMultiImageKeyboard,
    )

    await call.answer()
    kb = selectMultiImageKeyboard(
        model_name,
        group_number,
        MULTI_IMAGE_NUMBER,
        selected_indexes,
        job_id,
        model_key=model_key,
    )
    # Проверяем, отличается ли новая разметка от текущей
    current_markup = call.message.reply_markup
    markup_changed = False
    if (current_markup is None and kb is not None) or (current_markup is not None and kb is None):
        markup_changed = True
    elif current_markup is not None and kb is not None:
        try:
            markup_changed = current_markup.model_dump() != kb.model_dump()
        except Exception:
            markup_changed = current_markup != kb
    if markup_changed:
        await call.message.edit_reply_markup(reply_markup=kb)


async def multi_image_done(call: types.CallbackQuery, state: FSMContext):
    # Быстро отвечаем на callback query чтобы избежать timeout
    await call.answer()

    state_data = await state.get_data()
    _, full_model_key, _, job_id = call.data.split("|")

    # Извлекаем model_name и model_key из полного ключа
    if "_" in full_model_key:
        model_name, model_key = full_model_key.rsplit("_", 1)
    else:
        model_name = full_model_key
        model_key = None

    # В коллбэке передаётся короткий job_id, восстановим полный через helper
    message_id = call.message.message_id
    short_job_id = job_id
    resolved_job_id = resolve_job_id(
        state_data=state_data,
        model_name=model_name,
        model_key=model_key,
        message_id=message_id,
        short_job_id=short_job_id,
    )

    selected_indexes_raw = state_data.get("selected_indexes", {})
    if isinstance(selected_indexes_raw, list):
        # если по каким-то причинам лежит список, привяжем его к найденному job_id
        key_for_list = resolved_job_id or short_job_id
        selected_indexes_dict = {key_for_list: selected_indexes_raw}
    else:
        selected_indexes_dict = selected_indexes_raw

    # Определяем полный job_id
    full_job_id = resolved_job_id
    if not full_job_id:
        full_job_id = next(
            (k for k in selected_indexes_dict.keys() if isinstance(k, str) and k.startswith(short_job_id)),
            None,
        )

    if not full_job_id:
        # Не удалось определить задание — сообщаем пользователю и выходим без ошибки
        target_full_key = f"{model_name}_{model_key}" if model_key is not None else model_name
        logger.exception(
            f"[multi_image_done] job_id not found for message_id={message_id}, model_name={model_name}, short={short_job_id}, full_model_key={target_full_key}, selected_indexes_dict_keys={list(selected_indexes_dict.keys())}"
        )
        await call.answer("Не удалось определить задание. Попробуйте снова.", show_alert=True)
        return

    selected_indexes = selected_indexes_dict.get(full_job_id, [])

    if not selected_indexes:
        await call.answer(
            "Выберите хотя бы одно изображение!",
            show_alert=True,
        )
        return

    temp_dir = FACEFUSION_TEMP_IMAGES_FOLDER_PATH / f"{full_job_id}"
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
        job_id=full_job_id,
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
            process_image(fake_call, state, model_name, image_index, model_key=model_key),
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

    # Удаляем папку модели с оставшимися изображениями
    try:
        temp_path = os.path.join(
            FACEFUSION_TEMP_IMAGES_FOLDER_PATH,
            f"{full_job_id}",
        )
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
    except Exception as e:
        logger.error(f"Ошибка при удалении папки модели {model_name}: {e}")


# Добавление обработчиков
def hand_add():
    multi_image_router.callback_query.register(
        select_multi_image,
        lambda call: call.data.startswith("select_multi_image"),
    )
    multi_image_router.callback_query.register(
        multi_image_done,
        lambda call: call.data.startswith("multi_image_done"),
    )
