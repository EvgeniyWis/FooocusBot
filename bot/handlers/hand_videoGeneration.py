from utils.handlers import increaseCountInState, editMessageOrAnswer, appendDataToStateArray
from assets.mocks.links import MOCK_LINK_FOR_SAVE_VIDEO
from utils.handlers.videoGeneration import sendNextModelMessage, saveVideo
from utils import retryOperation, text
from utils.videos import generateVideo
from utils.generateImages.dataArray import getModelNameIndex, getDataByModelName
from utils.googleDrive.files import saveFile
from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards import video_generation_keyboards
from states import StartGenerationState
from logger import logger
import traceback
from InstanceBot import router
from datetime import datetime
from config import MOCK_MODE
from utils.handlers.startGeneration import waitStateArrayReplenishment


# Обработка нажатия кнопки "📹 Сгенерировать видео"
async def start_generate_video(call: types.CallbackQuery, state: FSMContext):
    temp = call.data.split("|")
    if len(temp) == 2:
        model_name = temp[1]
    else:
        model_name = None

    # Инициализируем стейты
    await state.update_data(sent_videos_count=0)
    await state.update_data(saved_videos_count=0)
    await state.update_data(generated_video_paths=[])

    # Отправляем сообщение для первой модели
    await sendNextModelMessage(state, call, model_name)


# Обработка нажатия кнопок режима генерации видео
async def handle_video_generation_mode_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем индекс модели
    model_name = call.data.split("|")[1]
    model_name_index = getModelNameIndex(model_name)

    # Получаем выбранный режим генерации видео
    mode = call.data.split("|")[2]

    # Если выбран режим "Написать свой промпт", то отправляем сообщение для ввода кастомного промпта
    if mode == "write_prompt":
        await state.update_data(model_name_for_video_generation=model_name)
        await editMessageOrAnswer(
        call,text.WRITE_PROMPT_FOR_VIDEO_TEXT.format(model_name, model_name_index))
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
async def handle_video_example_buttons(call: types.CallbackQuery, state: FSMContext):
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

    user_id = call.from_user.id
    await state.update_data(type_for_video_generation=type_for_video_generation)

    # Получаем название модели и url изображения
    data = await state.get_data()
    image_url = data["images_urls"][model_name]

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
    if "prompt_for_video" in data:
        custom_prompt = data["prompt_for_video"]
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
        call, text.GENERATE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index))
    
    # Удаляем из очереди текущую модель
    stateData = await state.get_data()
    stateData["saved_images_urls"] = [x for x in stateData["saved_images_urls"] if not (model_name in x)]
    await state.update_data(saved_images_urls=stateData["saved_images_urls"])
    
    # Отправляем следующую модель
    await sendNextModelMessage(state, call)

    # Добавляем повторно дату в стейт
    dataForUpdate = {f"{model_name}": image_url}
    stateData["saved_images_urls"].append(dataForUpdate)
    await state.update_data(saved_images_urls=stateData["saved_images_urls"])

    if type_for_video_generation == "work":
        # Увеличиваем счётчик того, сколько уже отправилось моделей
        await increaseCountInState(state, "sent_videos_count")

        # Проверяем, что модель последняя в генерации
        stateData = await state.get_data()
        if stateData["sent_videos_count"] == len(stateData["saved_images_urls"]):
            await call.message.answer(text.SAVING_VIDEOS_SUCCESS_TEXT, 
            reply_markup=video_generation_keyboards.saveVideoKeyboard())

    # Генерируем видео
    if MOCK_MODE:
        video_path = "FocuuusBot/bot/assets/mocks/mock_video.mp4"
    else:
        try:
            video_path = await retryOperation(generateVideo, 10, 1.5, video_example_prompt, image_url)
        except Exception as e:
            # Отправляем сообщение об ошибке
            traceback.print_exc()
            await editMessageOrAnswer(
            call,text.GENERATE_VIDEO_ERROR_TEXT.format(model_name, e))
            logger.error(f"Произошла ошибка при генерации видео для модели {model_name}: {e}")
            return
    
    # Изменяем сообщение про генерацию видео
    await message_for_edit.edit_text(text.GENERATE_VIDEO_SUCCESS_TEXT.format(model_name, model_name_index))

    # Сохраняем видео в стейт (только при рабочей генерации)
    if type_for_video_generation == "work":
        dataForUpdate = {"model_name": model_name, "video_path": video_path}
        await appendDataToStateArray(state, "generated_video_paths", dataForUpdate)
    else: # При тестовой просто отправляем юзеру результат генерации
        video = types.FSInputFile(video_path)
        await call.message.answer_video(video=video, caption=text.GENERATE_TEST_VIDEO_SUCCESS_TEXT.format(model_name, model_name_index), 
        reply_markup=video_generation_keyboards.generatedVideoKeyboard(f"generate_video|{model_name}", False))


# Хендлер для сохранения видео
async def start_save_video(call: types.CallbackQuery, state: FSMContext):
    # Ждём пока появится следующее сгенерированное видео в очереди
    generated_video_paths = await waitStateArrayReplenishment(state, "generated_video_paths", 
    ("sent_videos_count", "saved_videos_count"))

    # Получаем первую модель в очереди
    stateData = await state.get_data()
    model_name = generated_video_paths[0]["model_name"]
    video_path = generated_video_paths[0]["video_path"]

    # Получаем тип генерации
    type_for_video_generation = stateData["type_for_video_generation"]

    # Отправляем видео
    video = types.FSInputFile(video_path)
    if type_for_video_generation == "test":
        # TODO: режим генерации видео с видео-примерами временно отключен
        # if "video_example_index" in stateData:
        #     prefix = f"generate_video|{stateData['video_example_index']}|{model_name}"
        # else:
        #     prefix = f"generate_video|{model_name}"

        prefix = f"generate_video|{model_name}"

        await call.message.answer_video(video=video, caption=text.GENERATE_TEST_VIDEO_SUCCESS_TEXT.format(model_name), 
        reply_markup=video_generation_keyboards.generatedVideoKeyboard(prefix, False))

    elif type_for_video_generation == "work":
        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

        await call.message.answer_video(video=video, caption=text.GENERATE_VIDEO_SUCCESS_TEXT.format(model_name, model_name_index), 
        reply_markup=video_generation_keyboards.videoCorrectnessKeyboard(model_name))


# Хедлер для обработки ввода кастомного промпта для видео
async def write_prompt_for_video(message: types.Message, state: FSMContext):
    # Получаем данные
    prompt = message.text
    await state.update_data(prompt_for_video=prompt)
    data = await state.get_data()
    image_url = data["image_url"]

    # Отправляем видео
    model_name = data["model_name_for_video_generation"]

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)
    
    await message.answer_photo(
    photo=image_url,
    caption=text.WRITE_PROMPT_FOR_VIDEO_SUCCESS_TEXT.format(model_name, model_name_index, prompt),
    reply_markup=video_generation_keyboards.generatedVideoKeyboard(f"generate_video|{model_name}"))


# Обработка нажатия на кнопки корректности видео
async def handle_video_correctness_buttons(call: types.CallbackQuery, state: FSMContext):
    # Получаем тип кнопки
    temp = call.data.split("|")
    button_type = temp[1]
    model_name = temp[2]

    # Получаем данные
    stateData = await state.get_data()

    # Находим нужный путь к видео по модели
    for data in stateData["generated_video_paths"]:
        if data["model_name"] == model_name:
            video_path = data["video_path"]
            break

    # Получаем id папки и тд
    user_id = call.from_user.id
    modelData = await getDataByModelName(model_name)
    video_folder_id = modelData["video_folder_id"]
    now = datetime.now().strftime("%Y-%m-%d")

    if button_type == "correct":
        # Удаляем из очереди текущую модель
        stateData = await state.get_data()
        stateData["saved_images_urls"] = [x for x in stateData["saved_images_urls"] if not (model_name in x)]
        await state.update_data(saved_images_urls=stateData["saved_images_urls"])

        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

        # Отправляем сообщение о начале сохранения видео
        message_for_edit = await editMessageOrAnswer(
        call,text.SAVE_VIDEO_PROGRESS_TEXT.format(model_name, model_name_index))

        # Сохраняем видео
        if not MOCK_MODE:
            link = await saveFile(video_path, user_id, model_name, video_folder_id, now, False)
        else:
            link = MOCK_LINK_FOR_SAVE_VIDEO


# Обработка нажатия на кнопку "📹 Сгенерировать видео из изображения'"
async def start_generateVideoFromImage(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text.SEND_IMAGE_FOR_VIDEO_GENERATION)
    await state.set_state(StartGenerationState.send_image_for_video_generation)

    # Очищаем стейт от всех данных
    # TODO: убрать и сделать так, чтобы можно было генерить одновременно несколько видео
    # await state.update_data(image_file_ids_for_videoGenerationFromImage=[])
    # await state.update_data(prompts_for_videoGenerationFromImage={})
    # await state.update_data(video_paths=[])


# Обработка присылания изображения для генерации видео и запроса на присылания промпта
async def write_prompt_for_videoGenerationFromImage(message: types.Message, state: FSMContext):
    # Проверяем, есть ли изображение в сообщении
    if not message.photo:
        await message.answer(text.NO_IMAGE_FOR_VIDEO_GENERATION_ERROR_TEXT)
        return

    # Получаем file_id самого большого изображения
    photo = message.photo[-1]

    # Сохраняем его в массив в стейте
    stateData = await state.get_data()
    if "image_file_ids_for_videoGenerationFromImage" not in stateData:
        await state.update_data(image_file_ids_for_videoGenerationFromImage=[photo.file_id])
    else:
        stateData["image_file_ids_for_videoGenerationFromImage"].append(photo.file_id)
        await state.update_data(image_file_ids_for_videoGenerationFromImage=stateData["image_file_ids_for_videoGenerationFromImage"] + [photo.file_id])

    # Просим пользователя ввести промпт для генерации видео
    await state.set_state(None)
    await message.answer(text.WRITE_PROMPT_FOR_VIDEO_GENERATION_FOR_IMAGE_TEXT)
    await state.set_state(StartGenerationState.write_prompt_for_videoGenerationFromImage)


# Хендлер для обработки промпта для генерации видео из изображения
async def handle_prompt_for_videoGenerationFromImage(message: types.Message, state: FSMContext):
    # Получаем промпт
    prompt = message.text

    await state.update_data(prompt_for_videoGenerationFromImage=prompt)
    data = await state.get_data()
    image_file_id = data.get("image_file_id_for_videoGenerationFromImage")

    if not image_file_id:
        await message.answer(text.NO_IMAGE_FOR_VIDEO_GENERATION_ERROR_TEXT)
        return

    # Отправляем сообщение о прогрессе
    await message.answer(text.GENERATE_VIDEO_FROM_IMAGE_PROGRESS_TEXT)

    # Генерируем видео
    await generateVideoFromImage(image_file_id_index, prompt, message, state)


# Хендлер для обработки нажатия на кнопку "🔄 Перегенерировать видео"
async def handle_regenerate_video_from_image(call: types.CallbackQuery, state: FSMContext):
    # Получаем данные из стейта
    stateData = await state.get_data()
    image_file_id_index = int(call.data.split("|")[1])
    image_file_id = stateData["image_file_ids_for_videoGenerationFromImage"][image_file_id_index]
    prompt = stateData["prompts_for_videoGenerationFromImage"][image_file_id]
    
    # Отправляем сообщение о прогрессе
    await call.message.answer(text.GENERATE_VIDEO_FROM_IMAGE_PROGRESS_TEXT)

    # Генерируем видео
    await generateVideoFromImage(image_file_id_index, prompt, call.message, state)


# Хендлер для обработки нажатия на кнопку "💾 Сохранить видео"
async def handle_save_video(call: types.CallbackQuery, state: FSMContext):
    file_id_index = call.data.split("|")[1]
    await state.update_data(current_file_id_index=file_id_index)
    await state.set_state(StartGenerationState.ask_for_model_name_for_video_generation_from_image)
    await call.message.answer(text.SAVE_VIDEO_AND_WRITE_MODEL_NAME_TEXT)


# TODO:
# # Хендлер для обработки нажатия на кнопку "🔄 Перегенерировать видео"
# async def handle_regenerate_video_from_image(call: types.CallbackQuery, state: FSMContext):
#     # Получаем данные из стейта
#     stateData = await state.get_data()
#     image_file_id_index = int(call.data.split("|")[1])
#     image_file_id = stateData["image_file_ids_for_videoGenerationFromImage"][image_file_id_index]
#     prompt = stateData["prompts_for_videoGenerationFromImage"][image_file_id]
    
#     # Отправляем сообщение о прогрессе
#     await call.message.answer(text.GENERATE_VIDEO_FROM_IMAGE_PROGRESS_TEXT)

#     # Генерируем видео
#     await generateVideoFromImage(image_file_id_index, prompt, call.message, state)


# # Хендлер для обработки нажатия на кнопку "💾 Сохранить видео"
# async def handle_save_video(call: types.CallbackQuery, state: FSMContext):
#     file_id_index = call.data.split("|")[1]
#     await state.update_data(current_file_id_index=file_id_index)
#     await state.set_state(StartGenerationState.ask_for_model_name_for_video_generation_from_image)
#     await call.message.answer(text.SAVE_VIDEO_AND_WRITE_MODEL_NAME_TEXT)


# Хендлер для обработки ввода имени модели для сохранения видео
async def handle_model_name_for_video_generation_from_image(message: types.Message, state: FSMContext):
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
    # logger.info(f"Попытка получить путь к видео: {stateData['video_paths']} по индексу: {file_id_index}")
    # video_path = stateData["video_paths"][file_id_index]
    video_path = stateData["video_path"]

    # Сохраняем видео
    await state.set_state(None)
    await saveVideo(video_path, model_name, message)

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
    router.callback_query.register(start_generate_video, lambda call: call.data.startswith("start_generate_video"))

    router.callback_query.register(handle_video_generation_mode_buttons, lambda call: call.data.startswith("generate_video_mode"))

    router.callback_query.register(handle_video_example_buttons, lambda call: call.data.startswith("generate_video"))

    router.callback_query.register(start_save_video, lambda call: call.data == "start_save_video")

    router.message.register(write_prompt_for_video, StateFilter(StartGenerationState.write_prompt_for_video))

    router.callback_query.register(handle_video_correctness_buttons, 
    lambda call: call.data.startswith("video_correctness"))

    router.callback_query.register(
        start_generateVideoFromImage,
        lambda call: call.data == "generateVideoFromImage",
    )

    router.message.register(write_prompt_for_videoGenerationFromImage, 
    StateFilter(StartGenerationState.send_image_for_video_generation))

    router.message.register(handle_prompt_for_videoGenerationFromImage, StateFilter(StartGenerationState.write_prompt_for_videoGenerationFromImage))

    # TODO:
    # router.callback_query.register(handle_regenerate_video_from_image, 
    # lambda call: call.data.startswith("regenerate_video_from_image"))

    # router.callback_query.register(handle_save_video, lambda call: call.data.startswith("save_video"))

    router.message.register(handle_model_name_for_video_generation_from_image, StateFilter(StartGenerationState.ask_for_model_name_for_video_generation_from_image))
