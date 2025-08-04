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
    all_data_arrays = getAllDataArrays()

    # Ищем, в какой группе находится модель с таким названием
    for index, dataArray in enumerate(all_data_arrays):
        for data in dataArray:
            if data["model_name"] == model_name:
                result = index + 1

                if result == len(all_data_arrays):
                    return "extra"
                else:
                    return result

    # Если модель не найдена, то возвращаем None
    return None
