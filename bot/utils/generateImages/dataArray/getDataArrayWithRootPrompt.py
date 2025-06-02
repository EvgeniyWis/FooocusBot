from .getDataArrayBySettingNumber import getDataArrayBySettingNumber
from .getDataByModelName import getDataByModelName


# Функция для прибавления к изначальному промпту каждого элемента массива корневого промпта
async def getDataArrayWithRootPrompt(setting_number: int, root_prompt: str, model_names_for_generation: list[str] = None):
    # Если модели есть, то формируем из них массив
    if model_names_for_generation:
        dataArray = [await getDataByModelName(model_name) for model_name in model_names_for_generation]
        
    else: # Если нет, то берем по настройке
        dataArray = getDataArrayBySettingNumber(setting_number)

    for data in dataArray:
        data["json"]["input"]["prompt"] += " " + root_prompt

    return dataArray
