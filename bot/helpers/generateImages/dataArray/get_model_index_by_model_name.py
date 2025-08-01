from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


def get_model_index_by_model_name(model_name: str):
    """
    Получает индекс модели по её названию

    Args:
        model_name: str - название модели

    Returns:
        int | None - индекс модели или None, если модель не найдена
    """
    # Убираем +N, если он есть (например: "1+1" → "1")
    model_name = model_name.split("+")[0]

    # Получаем все группы
    all_groups = getAllDataArrays()

    # Ищем, в какой группе находится модель с таким названием
    for _, group in enumerate(all_groups):
        for dataArray in group:
            if dataArray["model_name"] == model_name:
                return dataArray["model_index"]

    return None
