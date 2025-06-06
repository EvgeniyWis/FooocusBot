import random

from aiogram.fsm.context import FSMContext
from logger import logger

from utils.handlers import appendDataToStateArray

from .getDataArrayBySettingNumber import getDataArrayBySettingNumber


# Функция для применения переменных рандомайзера к промптам массива данных
async def getDataArrayByRandomizer(state: FSMContext, setting_number: int):
    # Получаем массив данных
    stateData = await state.get_data()

    # Получаем переменные рандомайзера
    variable_names_for_randomizer = stateData.get("variable_names_for_randomizer", [])

    # Получаем массив данных
    dataArray = getDataArrayBySettingNumber(int(setting_number))

    # Проходимся по всем промптам для каждой переменной рандомайзера и формируем промпт
    for data in dataArray:
        for variable_name in variable_names_for_randomizer:
            # Получаем значения переменной
            variable_values = stateData.get(f"randomizer_{variable_name}_values", [])

            # Получаем случайное значение переменной
            random_variable_value = random.choice(variable_values)

            # Применяем значение переменной к промпу
            formated_prompt = f"{variable_name}: {random_variable_value};"

            data["json"]["input"]["prompt"] += " " + formated_prompt

            # Сохраняем промпт в стейт для перегенерации
            dataForUpdate = {f"{data['model_name']}": formated_prompt}
            await appendDataToStateArray(state, "randomizer_prompts", dataForUpdate)

    logger.info(f"Массив данных после применения переменных рандомайзера: {dataArray}")
    # Возвращаем массив данных
    return dataArray
