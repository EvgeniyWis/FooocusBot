from aiogram.fsm.context import FSMContext
from logger import logger

from bot.helpers.generateImages.dataArray.getDataArrayBySettingNumber import (
    getDataArrayBySettingNumber,
)
from bot.helpers.generateImages.dataArray.random_choice_variables_for_images import (
    random_choice_variables_for_images,
)
from bot.helpers.generateImages.get_data_array_by_model_indexes import (
    get_data_array_by_model_indexes,
)


# Функция для применения переменных рандомайзера к промптам массива данных
async def getDataArrayByRandomizer(
    state: FSMContext,
    setting_number: int | str,
    model_indexes_for_generation: list[int] = None,
):
    # Получаем массив данных
    state_data = await state.get_data()

    # Получаем переменные рандомайзера
    variable_names_for_randomizer = state_data.get(
        "variable_names_for_randomizer",
        [],
    )

    # Получаем массив данных
    if not model_indexes_for_generation:
        dataArray = getDataArrayBySettingNumber(setting_number)
    else:
        dataArray = await get_data_array_by_model_indexes(
            model_indexes_for_generation,
        )

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
    randomizer_prompts = []
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
        data["json"]["input"]["prompt"] = model_randomizer_prompt.replace(
            "\n",
            "",
        ) + data["json"]["input"]["prompt"].lstrip(" ")

        data_for_update = {f"{data['model_name']}": model_randomizer_prompt}

        logger.info(
            f"Данные для обновления: {data_for_update} для модели {data['model_name']}",
        )

        randomizer_prompts.append(data_for_update)

    await state.update_data(randomizer_prompts=randomizer_prompts)

    logger.info(
        f"Массив данных после применения переменных рандомайзера: {dataArray}",
    )
    # Возвращаем массив данных
    return dataArray
