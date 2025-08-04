from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


def getModelNameIndex(model_name: str):
    # Убираем +N, если он есть (например: "1+1" → "1")
    model_name = model_name.split("+")[0]  # fallback

    # Получаем все настройки
    all_settings = getAllDataArrays()

    # Ищем, в какой настройке находится модель с таким названием
    for index, setting in enumerate(all_settings):
        for dataArray in setting:
            if dataArray["model_name"] == model_name:
                if index == 0:
                    return setting.index(dataArray) + 1
                else:
                    return (
                        sum(len(setting) for setting in all_settings[:index])
                        + setting.index(dataArray)
                        + 1
                    )

    return None
