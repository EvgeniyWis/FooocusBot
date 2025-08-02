from bot.helpers.generateImages.dataArray.get_data_array_by_group_number import (
    get_data_array_by_group_number,
)


def get_model_index_in_group(model_index: int, group_number: int) -> int:
    group_data_array = get_data_array_by_group_number(group_number)
    for i, item in enumerate(group_data_array):
        if item["model_index"] == model_index:
            return i
    return -1  # Возвращаем -1 если элемент не найден
