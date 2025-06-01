from aiogram.fsm.context import FSMContext
from utils.handlers.startGeneration import waitStateArrayReplenishment
from utils import text
from aiogram import types
from keyboards import video_generation_keyboards
from utils.generateImages.dataArray import getModelNameIndex


# Функция для отправки сообщения о сохранении следующей модели
async def sendSavingNextModel(call: types.CallbackQuery, state: FSMContext) -> tuple[str, str]:
    # Ждём пока появится следующее сгенерированное видео в очереди
    generated_video_paths = await waitStateArrayReplenishment(
        state,
        "generated_video_paths",
        ("sent_videos_count", "saved_videos_count"),
        420
    )

    # Получаем первую модель в очереди
    model_name = generated_video_paths[0]["model_name"]
    video_path = generated_video_paths[0]["video_path"]

    # Получаем тип генерации
    stateData = await state.get_data()
    types_for_video_generation = stateData["types_for_video_generation"]
    type_for_video_generation = types_for_video_generation[0]["type"]

    # Отправляем видео
    video = types.FSInputFile(video_path)
    if type_for_video_generation == "test":
        # TODO: режим генерации видео с видео-примерами временно отключен
        # if "video_example_index" in stateData:
        #     prefix = f"generate_video|{stateData['video_example_index']}|{model_name}"
        # else:
        #     prefix = f"generate_video|{model_name}"

        prefix = f"generate_video|{model_name}"

        await call.message.answer_video(
            video=video,
            caption=text.GENERATE_TEST_VIDEO_SUCCESS_TEXT.format(model_name, model_name_index),
            reply_markup=video_generation_keyboards.generatedVideoKeyboard(
                prefix,
                False,
            ),
        )

    elif type_for_video_generation == "work":
        # Получаем индекс модели
        model_name_index = getModelNameIndex(model_name)

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


    return model_name, video_path
