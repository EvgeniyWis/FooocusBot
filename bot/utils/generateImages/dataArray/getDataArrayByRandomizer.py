from aiogram.fsm.context import FSMContext
from .getDataArrayBySettingNumber import getDataArrayBySettingNumber
import random
from logger import logger

# Функция для применения переменных рандомайзера к промптам массива данных
async def getDataArrayByRandomizer(state: FSMContext, setting_number: int):
    # Получаем массив данных
    stateData = await state.get_data()

    # Получаем переменные рандомайзера
    variable_names_for_randomizer = stateData["variable_names_for_randomizer"]

    # Получаем массив данных
    dataArray = getDataArrayBySettingNumber(setting_number)

    # Проходимся по всем промптам для каждой переменной рандомайзера и применяем её к промпу
    for data in dataArray:
        for variable_name in variable_names_for_randomizer:
            # Получаем значения переменной
            variable_values = stateData[f"randomizer_{variable_name}_values"]

            # Получаем случайное значение переменной
            random_variable_value = random.choice(variable_values)

            # Применяем значение переменной к промпу
            data["json"]["input"]["prompt"] += " " + f"{variable_name}: {random_variable_value};"

    logger.info(f"Массив данных после применения переменных рандомайзера: {dataArray}")
    # Возвращаем массив данных
    return dataArray
