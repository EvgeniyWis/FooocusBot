from .getDataArrayBySettingNumber import getDataArrayBySettingNumber

# Функция для прибавления к изначальному промпту каждого элемента массива корневого промпта
def getDataArrayWithRootPrompt(setting_number: int, root_prompt: str):
    dataArray = getDataArrayBySettingNumber(setting_number)
    
    for data in dataArray:
        data['input']['prompt'] = data['input']['prompt'] + " " + root_prompt

    return dataArray
