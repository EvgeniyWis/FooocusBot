from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


def get_all_model_names() -> list[str]:
    """
    Получает все имена моделей

    Returns:
        str - массив с именами моделей
    """

    all_data_arrays = getAllDataArrays()
    all_model_names = [data["model_name"] for dataArray in all_data_arrays for data in dataArray]
    all_model_names.sort()

    return all_model_names
