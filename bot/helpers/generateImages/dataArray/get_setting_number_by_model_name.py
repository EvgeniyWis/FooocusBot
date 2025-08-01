from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


# Функция для получения номера настройки по названию модели
def get_setting_number_by_model_name(model_name: str):
    """
    Получает номер настройки по названию модели

    Args:
        model_name: str - название модели

    Returns:
        int | str | None - номер настройки или None, если модель не найдена
    """
    # Получаем все группы
    all_data_arrays = getAllDataArrays()

    # Ищем, в какой группе находится модель с таким названием
    for _, dataArray in enumerate(all_data_arrays):
        for data in dataArray:
            if data["model_name"] == model_name:
                return data["setting_number"]

    # Если модель не найдена, то возвращаем None
    return None
