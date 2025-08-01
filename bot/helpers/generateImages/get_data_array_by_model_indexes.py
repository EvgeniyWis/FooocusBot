from bot.helpers.generateImages.dataArray.getDataByModelName import (
    getDataByModelName,
)
from bot.helpers.generateImages.dataArray.get_model_name_by_index import (
    get_model_name_by_index,
)


async def get_data_array_by_model_indexes(model_indexes: list[int]) -> list[dict]:
    """
    Получает массив индексом моделей, а на выход отдаёт массив данных этих моделей для генерации

    Args:
        model_indexes: list[int] - список индексов моделей

    Returns:
        list[dict] - массив данных моделей для генерации
    """
    model_names_for_generation = [
        get_model_name_by_index(model_index)
        for model_index in model_indexes
    ]
    data_array = [
        await getDataByModelName(model_name)
        for model_name in model_names_for_generation
    ]
    return data_array