import asyncio
import traceback

from aiogram import types
from aiogram.fsm.context import FSMContext
from logger import logger

from ... import text
from ...generateImages import (
    generateImageBlock,
    generateImages,
    generateImagesByAllSettings,
)
from ...generateImages.dataArray import (
    getDataArrayWithRootPrompt,
    getDataByModelName,
    getModelNameIndex,
)
import asyncio
from utils.generateImages.dataArray.getSettingNumberByModelName import getSettingNumberByModelName



# Функция для генерации изображения в зависимости от настроек
async def generateImagesInHandler(
    prompt: str,
    message: types.Message,
    state: FSMContext,
    user_id: int,
    is_test_generation: bool,
    setting_number: str,
    with_randomizer: bool = False,
):
    # Инициализируем стейт
    await state.update_data(models_for_generation_queue=[])
    await state.update_data(regenerate_images=[])
    await state.update_data(will_be_sent_generated_images_count=0)
    await state.update_data(finally_sent_generated_images_count=0)
    await state.update_data(total_images_count=0)
    await state.update_data(saved_videos_count=0)
    await state.update_data(media_groups_for_generation=None)
    await state.update_data(generation_step=1)

    # Генерируем изображения
    try:
        # Добавлена проверка на None для переменной message перед использованием
        if message is None:
            raise ValueError("message не может быть None")

        # Инициализация переменной message_for_edit перед её использованием
        message_for_edit = None

        if is_test_generation:
            if setting_number == "all":
                # Заполнение параметра is_test_generation в вызове функции
                result = await generateImagesByAllSettings(
                    message,
                    state,
                    user_id,
                    is_test_generation,
                )  # Отправляем сообщение о получении промпта
            else:
                # Инициализация переменной message_for_edit перед её использованием
                message_for_edit = await message.answer(
                    text.GET_PROMPT_SUCCESS_TEXT,
                )
                # Прибавляем к каждому элементу массива корневой промпт
                dataArray = getDataArrayWithRootPrompt(
                    int(setting_number),
                    prompt,
                )
                dataJSON = dataArray[0]["json"]
                model_name = dataArray[0]["model_name"]
                result = [
                    await generateImageBlock(
                        dataJSON,
                        model_name,
                        message_for_edit,
                        state,
                        user_id,
                        setting_number,
                        is_test_generation,
                    ),
                ]
        else:
            stateData = await state.get_data()
            model_names_for_generation = stateData.get("model_names_for_generation", [])
            logger.info(f"Получен список моделей для индивидуальной генерации: {model_names_for_generation}")

            if len(model_names_for_generation) > 0:
                for model_name in model_names_for_generation:
                    logger.info(f"Генерируем изображения для индивидуальной модели: {model_name}")

                    # Получаем порядковый номер модели
                    model_name_index = getModelNameIndex(model_name)

                    # Отправляем сообщение о генерации изображений по имени модели
                    await message.answer(text.GENERATE_IMAGES_BY_MODEL_NAME_TEXT.format(model_name, model_name_index))

                    # Получаем данные о модели
                    dataArray = await getDataByModelName(model_name)

                    # Прибавляем корневой промпт
                    dataArray["json"]['input']['prompt'] += " " + prompt
                    dataJSON = dataArray["json"]

                    # Получаем номер настройки по названию модели
                    setting_number = getSettingNumberByModelName(model_name)

                    # Запускаем задачу для генерации изображений
                    asyncio.create_task(generateImageBlock(dataJSON, model_name, message, state, user_id, setting_number, is_test_generation))
                return

            elif setting_number == "all":
                result = await generateImagesByAllSettings(
                    message,
                    state,
                    user_id,
                    is_test_generation,
                    True,
                )
            else:
                # Инициализация переменной message_for_edit перед её использованием
                message_for_edit = await message.answer(
                    text.GET_PROMPT_SUCCESS_TEXT,
                )
                await message_for_edit.pin()
                result = await generateImages(
                    int(setting_number),
                    prompt,
                    message_for_edit,
                    state,
                    user_id,
                    is_test_generation,
                    with_randomizer,
                )
                await message_for_edit.unpin()

        stateData = await state.get_data()

        if not is_test_generation:
            if result:
                if "stop_generation" not in stateData:
                    finally_sent_generated_images_count = stateData[
                        "finally_sent_generated_images_count"
                    ]
                    total_images_count = stateData["total_images_count"]

                    # Ждём когда список моделей для генерации станет пустым
                    while (
                        finally_sent_generated_images_count
                        < total_images_count
                    ):
                        stateData = await state.get_data()
                        finally_sent_generated_images_count = stateData[
                            "finally_sent_generated_images_count"
                        ]
                        total_images_count = stateData["total_images_count"]
                        await asyncio.sleep(10)

                    # Очищаем список медиагрупп
                    await state.update_data(media_groups_for_generation=None)
            else:
                if "stop_generation" not in stateData:
                    raise Exception(
                        "Произошла ошибка при генерации изображения",
                    )

    except Exception as e:
        try:
            await message_for_edit.unpin()
        except Exception:
            pass
        logger.error(f"Ошибка при генерации изображения: {e}")
        traceback.print_exc()
        await message.answer(text.GENERATION_IMAGE_ERROR_TEXT)
        await state.clear()
        return
