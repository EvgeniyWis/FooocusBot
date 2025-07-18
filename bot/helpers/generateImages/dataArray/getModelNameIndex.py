from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


# Функция для получения индекса модели
async def getModelNameIndex(model_name: str, user_id: int):
    # Получаем все настройки
    all_settings = await getAllDataArrays(user_id)

    # Ищем, в какой настройке находится модель с таким названием
    for index, setting in enumerate(all_settings):
        for dataArray in setting:
            if dataArray["model_name"] == model_name:
                if index == 0:
                    return setting.index(dataArray) + 1
                else:
                    # Берём длины всех массивов предыдущих настроек и суммируем их
                    return (
                        sum(len(setting) for setting in all_settings[:index])
                        + setting.index(dataArray)
                        + 1
                    )

    # Если модель не найдена, то возвращаем None
    return None
