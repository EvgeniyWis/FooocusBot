# Функция для получения данных генерации по названию модели
from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


async def getDataByModelName(model_name: str) -> dict:
    # Получаем все группы
    all_data_arrays = getAllDataArrays()

    # Ищем, в какой группе находится модель с таким названием
    for _, dataArray in enumerate(all_data_arrays):
        for data in dataArray:
            if data["model_name"] == model_name:
                return data

    # Если модель не найдена, то возвращаем пустой словарь
    return {}
