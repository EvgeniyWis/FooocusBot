from aiogram import types
from InstanceBot import router
from aiogram.filters import CommandStart, StateFilter
from InstanceBot import bot
from aiogram.fsm.context import FSMContext

# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    await message.answer("Привет, я бот для генерации изображений с помощью Focuuus API. Я могу создать изображение по вашему запросу. Введите ваш запрос и я сгенерирую изображение для вас.")

    await state.clear()


def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart())
