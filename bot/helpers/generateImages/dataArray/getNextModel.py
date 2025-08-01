from aiogram.fsm.context import FSMContext

from bot.helpers.generateImages.dataArray.get_data_array_by_group_number import (
    get_data_array_by_group_number,
)
from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)
from bot.logger import logger


# Функция для получения следующей модели в настройке
async def getNextModelInSetting(
    current_model: str,
    dataArrayBySettingNumber: list[dict],
):
    for index, dataArray in enumerate(dataArrayBySettingNumber):
        if current_model == dataArray["model_name"]:
            try:
                return dataArrayBySettingNumber[index + 1]["model_name"]
            except Exception:
                return False


# Функция для получения следующей модели
async def getNextModel(
    current_model: str,
    group_number: str,
    state: FSMContext,
):
    if group_number == "all":
        # Получаем все настройки
        dataArrays = getAllDataArrays()

        # Получаем текущую настройку
        state_data = await state.get_data()
        current_group_number = state_data[
            "current_group_number_for_unique_prompt"
        ]

        dataArrayBySettingNumber = dataArrays[current_group_number - 1]

        current_model_is_last_in_setting = (
            current_model == dataArrayBySettingNumber[-1]["model_name"]
        )

        logger.info(
            f"Текущая настройка: {current_group_number}. Является ли модель {current_model} последней в настройке: {current_model_is_last_in_setting}",
        )

        # Если текущая модель является последней в настройке, то получаем первую модель в следующей настройке
        if current_model_is_last_in_setting:
            if current_group_number == len(
                dataArrays,
            ):  # Если текущая настройка является последней, то False
                return False
            else:  # Если текущая настройка не является последней, то получаем первую модель в следующей настройке
                next_group_number = int(current_group_number) + 1
                await state.update_data(
                    current_group_number_for_unique_prompt=next_group_number,
                )
                dataArraysByNextSettingNumber = get_data_array_by_group_number(
                    next_group_number,
                )
                return dataArraysByNextSettingNumber[0]["model_name"]
        else:  # Если текущая модель не является последней в настройке, то получаем следующую модель в настройке
            return await getNextModelInSetting(
                current_model,
                dataArrayBySettingNumber,
            )
    else:
        # Получаем данные по номеру настройки
        dataArrayBySettingNumber = get_data_array_by_group_number(
            int(group_number),
        )

        return await getNextModelInSetting(
            current_model,
            dataArrayBySettingNumber,
        )
