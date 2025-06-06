from aiogram import types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from config import ALLOWED_USERS
from InstanceBot import router
from keyboards import start_generation_keyboards
from utils import text
from utils.jobs import cancelJobs


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    await state.set_state(None)

    if message.from_user.id not in ALLOWED_USERS:
        await message.answer(text.ACCESS_DENIED_TEXT)
        return

    # Если генерируются изображения в рабочей настройке, то отправляем сообщение без неё
    stateData = await state.get_data()
    if len(stateData.get("image_generation_jobs", [])) == 0:
        # Очищаем стейт
        await state.update_data(stop_generation=False)
        await state.update_data(generation_step=1)
        await state.update_data(prompts_for_regenerate_images=[])
        await state.update_data(regenerate_images=[])

        # Отправляем сообщение с кнопками
        await message.answer(
            text.START_TEXT, reply_markup=start_generation_keyboards.generationsTypeKeyboard(),
        )
    else:
        await message.answer(
            text.START_TEXT_WITHOUT_WORK_GENERATION, 
            reply_markup=start_generation_keyboards.generationsTypeKeyboard(with_work_generation=False),
        )


# Обработка команды /stop
async def stop_generation(message: types.Message, state: FSMContext):
    await state.update_data(stop_generation=True)
    await message.answer(text.STOP_GENERATION_TEXT, reply_markup=ReplyKeyboardRemove())

    # Отменяем все работы
    stateData = await state.get_data()
    await cancelJobs(stateData.get("image_generation_jobs", []))


# DEV: получение file id видео
# async def get_file_id(message: types.Message):
#     if message.video:
#         await message.answer(message.video.file_id)


# Добавление обработчиков
def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart())

    router.message.register(stop_generation, Command("stop"))

    # DEV: получение file id видео
    # router.message.register(get_file_id)


