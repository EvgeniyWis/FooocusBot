from aiogram.fsm.context import FSMContext
from logger import logger

from .getAllDataArrays import getAllDataArrays
from .getDataArrayBySettingNumber import getDataArrayBySettingNumber


# Функция для получения следующей модели в настройке
async def getNextModelInSetting(
    current_model: str, dataArrayBySettingNumber: list[dict],
):
    for index, dataArray in enumerate(dataArrayBySettingNumber):
        if current_model == dataArray["model_name"]:
            try:
                return dataArrayBySettingNumber[index + 1]["model_name"]
            except Exception:
                return False


# Функция для получения следующей модели
async def getNextModel(
    current_model: str, setting_number: str, state: FSMContext,
):
    if setting_number == "all":
        # Получаем все настройки
        dataArrays = getAllDataArrays()

        # Получаем текущую настройку
        stateData = await state.get_data()
        current_setting_number = stateData[
            "current_setting_number_for_unique_prompt"
        ]

        dataArrayBySettingNumber = dataArrays[current_setting_number - 1]

        current_model_is_last_in_setting = (
            current_model == dataArrayBySettingNumber[-1]["model_name"]
        )

        logger.info(
            f"Текущая настройка: {current_setting_number}. Является ли модель {current_model} последней в настройке: {current_model_is_last_in_setting}",
        )

        # Если текущая модель является последней в настройке, то получаем первую модель в следующей настройке
        if current_model_is_last_in_setting:
            if current_setting_number == len(
                dataArrays,
            ):  # Если текущая настройка является последней, то False
                return False
            else:  # Если текущая настройка не является последней, то получаем первую модель в следующей настройке
                next_setting_number = int(current_setting_number) + 1
                await state.update_data(
                    current_setting_number_for_unique_prompt=next_setting_number,
                )
                dataArraysByNextSettingNumber = getDataArrayBySettingNumber(
                    next_setting_number,
                )
                return dataArraysByNextSettingNumber[0]["model_name"]
        else:  # Если текущая модель не является последней в настройке, то получаем следующую модель в настройке
            return await getNextModelInSetting(
                current_model, dataArrayBySettingNumber,
            )
    else:
        # Получаем данные по номеру настройки
        dataArrayBySettingNumber = getDataArrayBySettingNumber(
            int(setting_number),
        )

        return await getNextModelInSetting(
            current_model, dataArrayBySettingNumber,
        )
