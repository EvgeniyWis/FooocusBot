from utils.generateImages import generateImageBlock
from aiogram import types
from aiogram.fsm.context import FSMContext
from utils.handlers import editMessageOrAnswer
from utils import text
from utils.generateImages.dataArray import getModelNameIndex, getDataByModelName


# Функция для перегенерации изображения
async def regenerateImage(model_name: str, call: types.CallbackQuery, state: FSMContext, setting_number: str):
    stateData = await state.get_data()
    is_test_generation = stateData["generations_type"] == "test"

    # Получаем индекс модели
    model_name_index = getModelNameIndex(model_name)

    # Получаем id пользователя
    user_id = call.from_user.id

    # Отправляем сообщение о перегенерации изображения
    await editMessageOrAnswer(
    call, text.REGENERATE_IMAGE_TEXT.format(model_name, model_name_index))

    # Получаем данные генерации по названию модели
    data = await getDataByModelName(model_name)
    return await generateImageBlock(data["json"], model_name, call.message, state, user_id, setting_number, is_test_generation, False)
