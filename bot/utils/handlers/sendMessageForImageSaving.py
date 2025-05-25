from aiogram import types
from aiogram.fsm.context import FSMContext
from utils.generateImages import getReferenceImage
from utils.generateImages.dataArray import getSettingNumberByModelName, getModelNameIndex
from utils import text
from keyboards import start_generation_keyboards


# Функция для отправки сообщения для сохранения изображения
async def sendMessageForImageSaving(call: types.CallbackQuery, state: FSMContext):
    # Получаем название модели, которая стоит первой в очереди
    stateData = await state.get_data()
    model_data = stateData["generated_images"][0]
    model_name = list(model_data.keys())[0]
    result_path = model_data[model_name]

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Получаем референсное изображение и добавляем его в медиагруппу
    media_group = []
    reference_image = await getReferenceImage(model_name)
    if reference_image:
        media_group.append(types.InputMediaPhoto(media=types.FSInputFile(reference_image)))

    # Добавляем итоговое изображение в медиагруппу
    media_group.append(types.InputMediaPhoto(media=types.FSInputFile(result_path)))

    # Отправляем медиагруппу
    await call.message.answer_media_group(media_group)

    # Получаем номер настройки
    setting_number = getSettingNumberByModelName(model_name)

    # Отправляем сообщение к референсному фото и итоговому изображению
    await call.message.answer(
        text.START_SAVE_IMAGE_TEXT.format(model_name, model_name_index), 
        reply_markup=start_generation_keyboards.saveImageKeyboard(model_name, setting_number))




