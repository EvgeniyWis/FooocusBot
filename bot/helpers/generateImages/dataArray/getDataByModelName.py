# Функция для получения данных генерации по названию модели
from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


async def getDataByModelName(model_name: str) -> dict:
    # Получаем все группы
    all_groups = getAllDataArrays()

    # Ищем, в какой группе находится модель с таким названием
    for group in all_groups:
        for dataArray in group:
            if dataArray["model_name"] == model_name:
                return dataArray

    # Если модель не найдена, то возвращаем пустой словарь
    return {}
