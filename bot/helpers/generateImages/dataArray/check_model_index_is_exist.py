from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)
from bot.app.core.logging import logger


def check_model_index_is_exist(model_index: int) -> bool:
    """
    Проверяет, существует ли модель с таким индексом

    Args:
        model_index: int - индекс модели

    Returns:
        bool - True, если модель с таким индексом существует, False - в противном случае
    """
    logger.info(f"Проверка существования модели с индексом {model_index}")
    
    all_data_arrays = getAllDataArrays()
    logger.info(f"Получено {len(all_data_arrays)} массивов данных для поиска")
    
    for data_array in all_data_arrays:
        for data in data_array:
            if data["model_index"] == model_index:
                logger.info(f"Модель с индексом {model_index} найдена в данных: {data}")
                return True

    logger.info(f"Модель с индексом {model_index} не найдена")
    return False
