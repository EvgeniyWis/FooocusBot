from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


# Функция для получения номера группы по названию модели
def get_group_number_by_model_name(model_name: str):
    """
    Получает номер группы по названию модели

    Args:
        model_name: str - название модели

    Returns:
        int | str | None - номер группы или None, если модель не найдена
    """
    # Получаем все группы
    all_groups = getAllDataArrays()

    # Ищем, в какой группе находится модель с таким названием
    for index, group in enumerate(all_groups):
        for dataArray in group:
            if dataArray["model_name"] == model_name:
                result = index + 1

                if result == len(all_groups):
                    return "extra"
                else:
                    return result

    # Если модель не найдена, то возвращаем None
    return None
