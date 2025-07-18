# Функция для получения данных генерации по названию модели
from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


async def getDataByModelName(model_name: str, user_id: int) -> dict:
    # Получаем все настройки
    all_settings = await getAllDataArrays(user_id)

    # Ищем, в какой настройке находится модель с таким названием
    for setting in all_settings:
        for dataArray in setting:
            if dataArray["model_name"] == model_name:
                return dataArray

    # Если модель не найдена, то возвращаем пустой словарь
    return {}
