from bot.utils.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


# Функция для получения имени модели по его номеру
def getModelNameByIndex(index):
    # Получаем все массивы данных из всех настроек
    all_settings = getAllDataArrays()

    # Преобразуем индекс в число
    index = int(index)

    # Проверяем, что индекс больше 0
    if index <= 0:
        return None

    # Уменьшаем индекс на 1, так как в массиве индексация с 0
    index = index - 1

    # Проходим по всем настройкам
    current_length = 0
    for setting in all_settings:
        # Если индекс меньше длины текущей настройки + текущая длина,
        # значит модель находится в этой настройке
        if index < len(setting) + current_length:
            # Возвращаем имя модели из текущей настройки
            return setting[index - current_length]["model_name"]
        current_length += len(setting)

    # Если индекс больше, чем общее количество моделей
    return None
