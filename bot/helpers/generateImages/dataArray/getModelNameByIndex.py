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

    all_groups = getAllDataArrays()

    current_length = 0
    for group in all_groups:
        if base_index_int < len(group) + current_length:
            return group[base_index_int - current_length]["model_name"]
        current_length += len(group)

    return None
