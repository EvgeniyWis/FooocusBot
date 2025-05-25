from utils.generateImages.dataArray import getAllDataArrays

# Функция для получения номера настройки по названию модели
def getSettingNumberByModelName(model_name: str):
    # Получаем все настройки
    all_settings = getAllDataArrays()

    # Ищем, в какой настройке находится модель с таким названием
    for index, setting in enumerate(all_settings):
        for dataArray in setting:
            if dataArray["model_name"] == model_name:
                return index + 1
            
    # Если модель не найдена, то возвращаем None
    return None
