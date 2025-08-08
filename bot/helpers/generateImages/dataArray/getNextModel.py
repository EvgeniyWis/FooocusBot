from aiogram.fsm.context import FSMContext

from bot.helpers.generateImages.dataArray.get_data_array_by_group_number import (
    get_data_array_by_group_number,
)
from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)
from bot.app.core.logging import logger


# Функция для получения следующей модели в группе
async def get_next_model_in_group(
    current_model: str,
    dataArrayByGroupNumber: list[dict],
):
    for index, dataArray in enumerate(dataArrayByGroupNumber):
        if current_model == dataArray["model_name"]:
            try:
                return dataArrayByGroupNumber[index + 1]["model_name"]
            except Exception:
                return False


# Функция для получения следующей модели
async def getNextModel(
    current_model: str,
    group_number: str,
    state: FSMContext,
):
    if group_number == "all":
        # Получаем все группы
        dataArrays = getAllDataArrays()

        # Получаем текущую группу
        state_data = await state.get_data()
        current_group_number = state_data[
            "current_group_number_for_unique_prompt"
        ]

        dataArrayByGroupNumber = dataArrays[current_group_number - 1]

        current_model_is_last_in_group = (
            current_model == dataArrayByGroupNumber[-1]["model_name"]
        )

        logger.info(
            f"Текущая группа: {current_group_number}. Является ли модель {current_model} последней в группе: {current_model_is_last_in_group}",
        )

        # Если текущая модель является последней в группе, то получаем первую модель в следующей группе
        if current_model_is_last_in_group:
            if current_group_number == len(
                dataArrays,
            ):  # Если текущая группа является последней, то False
                return False
            else:  # Если текущая группа не является последней, то получаем первую модель в следующей группе
                next_group_number = int(current_group_number) + 1
                await state.update_data(
                    current_group_number_for_unique_prompt=next_group_number,
                )
                dataArraysByNextGroupNumber = get_data_array_by_group_number(
                    next_group_number,
                )
                return dataArraysByNextGroupNumber[0]["model_name"]
        else:  # Если текущая модель не является последней в группе, то получаем следующую модель в группе
            return await get_next_model_in_group(
                current_model,
                dataArrayByGroupNumber,
            )
    else:
        # Получаем данные по номеру группы
        dataArrayByGroupNumber = get_data_array_by_group_number(
            int(group_number),
        )

        return await get_next_model_in_group(
            current_model,
            dataArrayByGroupNumber,
        )
