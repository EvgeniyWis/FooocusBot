import asyncio
import os
import traceback
from datetime import datetime

from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from assets.mocks.links import MOCK_LINK_FOR_SAVE_VIDEO
from config import MOCK_MODE, TEMP_IMAGE_FILES_DIR
from InstanceBot import bot, router
from keyboards import video_generation_keyboards
from logger import logger
from states import StartGenerationState
from utils import retryOperation, text
from utils.generateImages.dataArray import (
    getDataByModelName,
    getModelNameIndex,
)
from utils.googleDrive.files import saveFile
from utils.handlers import (
    editMessageOrAnswer,
)
from utils.handlers.videoGeneration import saveVideo
from utils.videos import generateVideo
from utils.googleDrive.folders import getFolderDataByID
from utils.handlers import appendDataToStateArray


# Обработка нажатия кнопки "📹 Сгенерировать видео"
async def start_generate_video(call: types.CallbackQuery, state: FSMContext):
    # Получаем название модели
    model_name = call.data.split("|")[1]

    # Удаляем видео из папки temp/videos, если оно есть
    try:
        stateData = await state.get_data()
        if "video_path" in stateData:
            os.remove(stateData["video_path"])
    except Exception as e:
        logger.error(f"Ошибка при удалении видео из папки temp/videos: {e}")

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение для выбора видео-примеров
    await editMessageOrAnswer(
        call,text.SELECT_VIDEO_TYPE_GENERATION_TEXT.format(model_name, model_name_index),
        reply_markup=video_generation_keyboards.videoWritePromptKeyboard(model_name))


# Обработка нажатия кнопок режима генерации видео
async def handle_video_generation_mode_buttons(
    call: types.CallbackQuery,
    state: FSMContext,
):
    # Получаем индекс модели
    temp = call.data.split("|")
    model_name = temp[1]
    model_name_index = getModelNameIndex(model_name)

    # Получаем выбранный режим генерации видео
    mode = temp[2]

    # Если выбран режим "Написать свой промпт", то отправляем сообщение для ввода кастомного промпта
    if mode == "write_prompt":
        await state.update_data(model_name_for_video_generation=model_name)
        await editMessageOrAnswer(
            call,
            text.WRITE_PROMPT_FOR_VIDEO_TEXT.format(
                model_name,
                model_name_index,
            ),
        )
        await state.set_state(StartGenerationState.write_prompt_for_video)
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
    # Получаем индекс видео-примера и тип кнопки
    temp = call.data.split("|")

    if len(temp) == 4:
        # TODO: режим генерации видео с видео-примерами временно отключен
        # index = int(temp[1])
        model_name = temp[2]
        type_for_video_generation = temp[3]
        # await state.update_data(video_example_index=index)
    else:
        model_name = temp[1]
        type_for_video_generation = temp[2]

    # Получаем название модели и url изображения
    stateData = await state.get_data()
    image_url_dict = next((item for item in stateData["saved_images_urls"] if model_name in item.keys()), None)
    
    # Получаем URL изображения из словаря
    image_url = image_url_dict[model_name] if image_url_dict else None

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
    if "prompt_for_video" in stateData:
        custom_prompt = stateData["prompt_for_video"]
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

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение про генерацию видео
    message_for_edit = await editMessageOrAnswer(
        call,
        text.GENERATE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index),
    )

    # Генерируем видео
    if MOCK_MODE:
        video_path = "FocuuusBot/bot/assets/mocks/mock_video.mp4"
    else:
        try:
            video_path = await retryOperation(
                generateVideo,
                10,
                1.5,
                video_example_prompt,
                image_url,
            )
        except Exception as e:
            # Отправляем сообщение об ошибке
            traceback.print_exc()
            await editMessageOrAnswer(
                call,
                text.GENERATE_VIDEO_ERROR_TEXT.format(model_name, model_name_index, e),
            )
            logger.error(
                f"Произошла ошибка при генерации видео для модели {model_name}: {e}",
            )
            return
    
    if not video_path:
        await call.message.answer(text.GENERATE_VIDEO_ERROR_TEXT.format(model_name, model_name_index, "Не удалось сгенерировать видео"))
        return
    
    # Добавляем путь к видео в стейт
    dataForUpdate = {f"{model_name}": video_path}
    await appendDataToStateArray(state, "video_paths", dataForUpdate)

    # Изменяем сообщение про генерацию видео
    await message_for_edit.edit_text(
        text.GENERATE_VIDEO_SUCCESS_TEXT.format(model_name, model_name_index),
    )

    # Отправляем видео юзеру
    video = types.FSInputFile(video_path)
    prefix = f"generate_video|{model_name}"
    if type_for_video_generation == "work":
        await call.message.answer_video(
            video=video,
            caption=text.GENERATE_VIDEO_SUCCESS_TEXT.format(
                model_name,
                model_name_index,
            ),
            reply_markup=video_generation_keyboards.videoCorrectnessKeyboard(
                model_name,
            ),
        )
    else:  # При тестовой просто отправляем юзеру результат генерации
        await call.message.answer_video(
            video=video,
            caption=text.GENERATE_TEST_VIDEO_SUCCESS_TEXT.format(
                model_name,
                model_name_index,
            ),
            reply_markup=video_generation_keyboards.generatedVideoKeyboard(
                prefix,
                False,
            ),
        )



# Хедлер для обработки ввода кастомного промпта для видео
async def write_prompt_for_video(message: types.Message, state: FSMContext):
    # Получаем данные
    prompt = message.text
    await state.update_data(prompt_for_video=prompt)
    stateData = await state.get_data()
    model_name = stateData["model_name_for_video_generation"]
    image_url_dict = next((item for item in stateData["saved_images_urls"] if model_name in item.keys()), None)
    
    # Получаем URL изображения из словаря
    image_url = image_url_dict[model_name] if image_url_dict else None
    
    if not image_url:
        await message.answer("Ошибка: не удалось найти URL изображения")
        return

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    logger.info(f"URL изображения для генерации видео модели {model_name}: {image_url}")
    try:
        await message.answer_photo(
            photo=image_url,
            caption=text.WRITE_PROMPT_FOR_VIDEO_SUCCESS_TEXT.format(
                model_name,
                model_name_index,
                prompt,
            ),
            reply_markup=video_generation_keyboards.videoGenerationTypeKeyboard(
                model_name,
                True,
            ),
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке фото: {e}")
        # Если не удалось отправить фото, отправляем только текст
        await message.answer(
            text.WRITE_PROMPT_FOR_VIDEO_SUCCESS_TEXT.format(
                model_name,
                model_name_index,
                prompt,
            ),
            reply_markup=video_generation_keyboards.videoGenerationTypeKeyboard(
                model_name,
                True,
            ),
        )


# Обработка нажатия на кнопки корректности видео
async def handle_video_correctness_buttons(
    call: types.CallbackQuery,
    state: FSMContext,
):
    # Получаем тип кнопки
    temp = call.data.split("|")
    model_name = temp[2]

    # Получаем данные
    stateData = await state.get_data()

    # Получаем id папки и тд
    user_id = call.from_user.id
    modelData = await getDataByModelName(model_name)
    video_folder_id = modelData["video_folder_id"]
    now = datetime.now().strftime("%Y-%m-%d")

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Отправляем сообщение о начале сохранения видео
    message_for_edit = await editMessageOrAnswer(
        call,
        text.SAVE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index),
    )

    video_path = next((item for item in stateData["video_paths"] if model_name in item.keys()), None)
    video_path = video_path[model_name]

    # Сохраняем видео
    if not MOCK_MODE:
        link = await saveFile(
            video_path,
            user_id,
            model_name,
            video_folder_id,
            now,
            False,
        )
    else:
        link = MOCK_LINK_FOR_SAVE_VIDEO

    if not link:
        await editMessageOrAnswer(
    call,text.SAVE_FILE_ERROR_TEXT)
        return
    
    # Получаем данные родительской папки
    folder = getFolderDataByID(video_folder_id)
    parent_folder_id = folder['parents'][0]
    parent_folder = getFolderDataByID(parent_folder_id)

    logger.info(f"Данные папки по id {video_folder_id}: {folder}")

    # Удаляем сообщение про генерацию видео
    await bot.delete_message(user_id, message_for_edit.message_id)

    # Отправляем сообщение о сохранении видео
    await message_for_edit.answer(text.SAVE_VIDEO_SUCCESS_TEXT
    .format(link, model_name, parent_folder['webViewLink'], model_name_index)
    )

    # Удаляем видео из папки temp/videos
    if not MOCK_MODE:
        os.remove(video_path)


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
    # await state.update_data(video_paths=[])


# Обработка присылания изображения для генерации видео и запроса на присылания промпта
async def write_prompt_for_videoGenerationFromImage(
    message: types.Message,
    state: FSMContext,
):
    # Проверяем, есть ли изображение в сообщении
    if not message.photo:
        await message.answer(text.NO_IMAGE_FOR_VIDEO_GENERATION_ERROR_TEXT)
        return

    # Получаем file_id самого большого изображения
    photo = message.photo[-1]
    await state.update_data(
        image_file_id_for_videoGenerationFromImage=photo.file_id,
    )

    # Просим пользователя ввести промпт для генерации видео
    await state.set_state(None)
    await message.answer(text.WRITE_PROMPT_FOR_VIDEO_GENERATION_FOR_IMAGE_TEXT)
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
    stateData = await state.get_data()
    image_file_id = stateData.get("image_file_id_for_videoGenerationFromImage")

    if not image_file_id:
        await message.answer(text.NO_IMAGE_FOR_VIDEO_GENERATION_ERROR_TEXT)
        return

    # Отправляем сообщение о прогрессе
    await message.answer(text.GENERATE_VIDEO_FROM_IMAGE_PROGRESS_TEXT)

    try:
        # Скачиваем изображение (file_id) и получаем путь к файлу
        # Для этого используем bot.download_file и сохраняем во временную папку
        try:
            file = await asyncio.wait_for(
                bot.get_file(image_file_id),
                timeout=30,
            )
        except TimeoutError:
            await message.answer(
                "⏰ Время ожидания получения файла Telegram истекло. Попробуйте позже.",
            )
            raise TimeoutError(
                "Время ожидания получения файла Telegram истекло.",
            )

        file_path = file.file_path
        temp_path = f"{TEMP_IMAGE_FILES_DIR}/{image_file_id}.jpg"

        try:
            await asyncio.wait_for(
                bot.download_file(file_path, temp_path),
                timeout=60,
            )
        except TimeoutError:
            await message.answer(
                "⏰ Время ожидания скачивания файла Telegram истекло. Попробуйте позже.",
            )
            raise TimeoutError(
                "Время ожидания скачивания файла Telegram истекло.",
            )

        # Генерируем видео
        video_path = await retryOperation(
            generateVideo,
            10,
            1.5,
            prompt,
            None,
            temp_path,
        )
        await state.update_data(video_path_for_videoGenerationFromImage=video_path)

        video = types.FSInputFile(video_path)
        await message.answer_video(
            video=video,
            caption=text.GENERATE_VIDEO_FROM_IMAGE_SUCCESS_TEXT,
        )

        # Спрашиваем, в папку какой модели сохранить видео
        await state.set_state(None)
        await message.answer(
            text.ASK_FOR_MODEL_NAME_FOR_VIDEO_GENERATION_FROM_IMAGE_TEXT,
        )
        await state.set_state(
            StartGenerationState.ask_for_model_name_for_video_generation_from_image,
        )

        # Удаляем временное изображение
        os.remove(temp_path)
    except Exception as e:
        traceback.print_exc()
        await message.answer(
            text.GENERATE_VIDEO_FROM_IMAGE_ERROR_TEXT.format(e),
        )
        logger.error(f"Ошибка при генерации видео из изображения: {e}")


# Хендлер для обработки ввода имени модели для сохранения видео
async def handle_model_name_for_video_generation_from_image(
    message: types.Message,
    state: FSMContext,
):
    # Получаем данные
    stateData = await state.get_data()
    # file_id_index = int(stateData["current_file_id_index"])

    # Получаем данные по имени модели
    model_name = message.text

    # Если такой модели не существует, то просим ввести другое название
    if not await getDataByModelName(model_name):
        await message.answer(text.MODEL_NOT_FOUND_TEXT)
        return

    # Получаем путь к видео
    video_path = stateData["video_path_for_videoGenerationFromImage"]

    # Сохраняем видео
    await state.set_state(None)
    await saveVideo(video_path, model_name, message)

    # TODO: вернуть
    # try:
    #     # Очищаем все стейты от текущих данных
    #     await state.update_data(current_file_id_index=None)

    #     # Получаем file_id изображения, которое нужно удалить
    #     image_file_id = stateData["image_file_ids_for_videoGenerationFromImage"][file_id_index]
    #     # Удаляем видео из списка и обновляем state
    #     updated_video_paths = stateData["video_paths"]
    #     updated_video_paths.pop(file_id_index)
    #     await state.update_data(video_paths=updated_video_paths)

    #     # Удаляем file_id из списка и обновляем state
    #     updated_image_file_ids = stateData["image_file_ids_for_videoGenerationFromImage"]
    #     updated_image_file_ids.pop(file_id_index)
    #     await state.update_data(image_file_ids_for_videoGenerationFromImage=updated_image_file_ids)

    #     # Удаляем промпт по file_id и обновляем state
    #     updated_prompts = stateData["prompts_for_videoGenerationFromImage"]
    #     updated_prompts.pop(image_file_id)
    #     await state.update_data(prompts_for_videoGenerationFromImage=updated_prompts)
    #     logger.info(f"Удалены данные из массивов: {updated_video_paths}, {updated_image_file_ids}, {updated_prompts}")
    # except Exception as e:
    #     logger.error(f"Произошла ошибка при сохранении видео: {e}")


# Добавление обработчиков
def hand_add():
    router.callback_query.register(
        start_generate_video,
        lambda call: call.data.startswith("start_generate_video"),
    )

    router.callback_query.register(
        handle_video_generation_mode_buttons,
        lambda call: call.data.startswith("generate_video_mode"),
    )

    router.callback_query.register(
        handle_video_example_buttons,
        lambda call: call.data.startswith("generate_video"),
    )

    router.message.register(
        write_prompt_for_video,
        StateFilter(StartGenerationState.write_prompt_for_video),
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