from .getAllDataArrays import getAllDataArrays

# Функция для получения индекса модели
def getModelNameIndex(model_name: str):
    # Получаем все настройки
    all_settings = getAllDataArrays()

    # Ищем, в какой настройке находится модель с таким названием
    for setting in all_settings:
        for dataArray in setting:
            if dataArray["model_name"] == model_name:
                return setting.index(dataArray) + 1

    # Если модель не найдена, то возвращаем None
    return None

