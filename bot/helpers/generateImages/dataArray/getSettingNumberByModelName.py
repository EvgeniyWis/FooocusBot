from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


# Функция для получения номера настройки по названию модели
async def getSettingNumberByModelName(model_name: str, user_id):
    # Получаем все настройки
    all_settings = await getAllDataArrays(user_id)

    # Ищем, в какой настройке находится модель с таким названием
    for index, setting in enumerate(all_settings):
        for dataArray in setting:
            if dataArray["model_name"] == model_name:
                result = index + 1

                if result == 5:
                    return "extra"
                else:
                    return result

    # Если модель не найдена, то возвращаем None
    return None
