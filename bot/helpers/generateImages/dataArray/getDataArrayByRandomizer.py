from aiogram.fsm.context import FSMContext
from logger import logger

from bot.helpers.generateImages.dataArray.getDataArrayBySettingNumber import (
    getDataArrayBySettingNumber,
)
from bot.helpers.generateImages.dataArray.random_choice_variables_for_images import (
    random_choice_variables_for_images,
)
from bot.utils.handlers import appendDataToStateArray


# Функция для применения переменных рандомайзера к промптам массива данных
async def getDataArrayByRandomizer(
    state: FSMContext,
    setting_number: int | str,
):
    # Получаем массив данных
    state_data = await state.get_data()

    # Получаем переменные рандомайзера
    variable_names_for_randomizer = state_data.get(
        "variable_names_for_randomizer",
        [],
    )

    # Получаем массив данных
    dataArray = getDataArrayBySettingNumber(setting_number)

    logger.info(
        f"Массив данных до применения переменных рандомайзера: {dataArray} для настройки {setting_number}",
    )

    generators = {}
    for variable_name in variable_names_for_randomizer:
        variable_values = state_data.get(
            f"randomizer_{variable_name}_values",
            [],
        )
        if variable_values:
            generators[variable_name] = random_choice_variables_for_images(
                variable_values,
            )
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

            formated_prompt = f"{variable_name}: {random_variable_value}; "

            model_randomizer_prompt += formated_prompt

        # Добавляем к постонному промпту промпт рандомайзера
        data["json"]["input"]["prompt"] = (
            model_randomizer_prompt.replace("\n", "")
            + data["json"]["input"]["prompt"].lstrip(" ")
        )

        data_for_update = {
            "model_name": data["model_name"],
            "image_index": data.get(
                "image_index",
                0,
            ),
            "prompt": model_randomizer_prompt,
        }
        await appendDataToStateArray(
            state,
            "randomizer_prompts",
            data_for_update,
            unique_keys=("model_name", "image_index"),
        )

    logger.info(
        f"Массив данных после применения переменных рандомайзера: {dataArray}",
    )
    # Возвращаем массив данных
    return dataArray
