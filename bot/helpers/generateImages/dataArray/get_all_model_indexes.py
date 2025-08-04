from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


def get_all_model_indexes() -> str:
    """
    Получает все индексы моделей

    Returns:
        str - строка с всеми индексами моделей
    """

    all_data_arrays = getAllDataArrays()
    all_model_indexes = [data["model_index"] for dataArray in all_data_arrays for data in dataArray]
    all_model_indexes.sort()
    all_model_indexes_str = ", ".join(map(str, all_model_indexes))

    return all_model_indexes_str
