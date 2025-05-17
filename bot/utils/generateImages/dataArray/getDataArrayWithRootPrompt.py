from .getDataArrayBySettingNumber import getDataArrayBySettingNumber

# Функция для прибавления к изначальному промпту каждого элемента массива корневого промпта
def getDataArrayWithRootPrompt(setting_number: int, root_prompt: str):
    dataArray = getDataArrayBySettingNumber(setting_number)
    
    for data in dataArray:
        data["json"]['input']['prompt'] += " " + root_prompt

    return dataArray
