import random

from aiogram.fsm.context import FSMContext
from logger import logger

from utils.handlers import appendDataToStateArray

from .getDataArrayBySettingNumber import getDataArrayBySettingNumber
from .random_choice_variables_for_images import random_choice_variables_for_images


# Функция для применения переменных рандомайзера к промптам массива данных
async def getDataArrayByRandomizer(state: FSMContext, setting_number: int):
    # Получаем массив данных
    stateData = await state.get_data()

    # Получаем переменные рандомайзера
    variable_names_for_randomizer = stateData.get("variable_names_for_randomizer", [])

    # Получаем массив данных
    dataArray = getDataArrayBySettingNumber(int(setting_number))

    generators = {}
    for variable_name in variable_names_for_randomizer:
        variable_values = stateData.get(f"randomizer_{variable_name}_values", [])
        if variable_values:
            generators[variable_name] = random_choice_variables_for_images(variable_values)
        else:
            logger.warning(f"Нет значений для переменной '{variable_name}'")
    
    # Проходимся по всем промптам для каждой переменной рандомайзера и формируем промпт
    for data in dataArray:
        model_randomizer_prompt = ""

        for variable_name in variable_names_for_randomizer:
            gen = generators.get(variable_name)
            if not gen:
                continue
            random_variable_value = next(gen)
            
            formated_prompt = f"{variable_name}: {random_variable_value};"

            model_randomizer_prompt += formated_prompt

        # Прибавляем к постоянному промпту промпт рандомайзера      
        data["json"]["input"]["prompt"] = model_randomizer_prompt.replace("\n", " ") + " " + data["json"]["input"]["prompt"]

        # Сохраняем промпт в стейт для перегенерации
        dataForUpdate = {f"{data['model_name']}": model_randomizer_prompt}
        await appendDataToStateArray(state, "randomizer_prompts", dataForUpdate)

    logger.info(f"Массив данных после применения переменных рандомайзера: {dataArray}")
    # Возвращаем массив данных
    return dataArray
