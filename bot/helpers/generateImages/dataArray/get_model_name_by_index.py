from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


def get_model_name_by_index(index: int | str):
    """
    Получает название модели по её индексу

    Args:
        index: int | str - индекс модели

    Returns:
        str | None - название модели или None, если модель не найдена
    """
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
    
    # Получаем все группы
    all_groups = getAllDataArrays()

    # Ищем, в какой группе находится модель с таким названием
    for _, group in enumerate(all_groups):
        for dataArray in group:
            if dataArray["model_index"] == base_index_int:
                return dataArray["model_name"]

    return None
