# Функция для получения данных генерации по названию модели
from utils.generateImages.dataArray.getAllDataArrays import getAllDataArrays


async def getDataByModelName(model_name: str) -> dict:
    # Получаем все настройки
    all_settings = getAllDataArrays()

    # Ищем, в какой настройке находится модель с таким названием
    for setting in all_settings:
        for dataArray in setting:
            if dataArray["model_name"] == model_name:
                return dataArray

    # Если модель не найдена, то возвращаем None
    return None


