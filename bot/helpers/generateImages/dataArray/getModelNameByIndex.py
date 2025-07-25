from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


def getModelNameByIndex(index):
    if not isinstance(index, str):
        index = str(index)

    # Обрезаем суффикс +N, если он есть
    base_index = index.split("+")[0]

    try:
        base_index_int = int(base_index)
    except ValueError:
        return None  # или raise, если нужно

    if base_index_int <= 0:
        return None

    base_index_int -= 1

    all_settings = getAllDataArrays()

    current_length = 0
    for setting in all_settings:
        if base_index_int < len(setting) + current_length:
            return setting[base_index_int - current_length]["model_name"]
        current_length += len(setting)

    return None
