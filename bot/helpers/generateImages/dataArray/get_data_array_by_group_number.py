from bot.helpers.generateImages.dataArray.groups.extra_group.get_data_array import (
    extra_group_get_data_array,
)
from bot.helpers.generateImages.dataArray.groups.first_group.get_data_array import (
    first_group_get_data_array,
)
from bot.helpers.generateImages.dataArray.groups.second_group.get_data_array import (
    second_group_get_data_array,
)


def get_data_array_by_group_number(group_number: int | str):
    """
    Получает массив данных для группы по номеру группы

    Args:
        group_number: int | str - номер группы

    Returns:
        list[dict] - массив данных для группы
    """
    # Если передана строка и она является числом, преобразуем её в число
    if isinstance(group_number, str):
        if group_number.isdigit():
            group_number = int(group_number)

    if group_number == 1:
        return first_group_get_data_array()
    elif group_number == 2:
        return second_group_get_data_array()
    elif group_number == "extra":
        return extra_group_get_data_array()

    raise ValueError(f"Неизвестный номер группы: {group_number}")