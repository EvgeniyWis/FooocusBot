from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)
from bot.app.core.logging import logger


def get_group_model_indexes(group_number: int | str) -> str:
    """
    Получает все индексы моделей, принадлежащие данной группе

    Args:
        group_number: int | str - номер группы или "all" для всех групп

    Returns:
        str - строка с всеми индексами моделей
    """
    logger.info(f"Получение индексов моделей для группы {group_number}")
    
    all_data_arrays = getAllDataArrays()
    logger.info(f"Получено {len(all_data_arrays)} массивов данных")
    
    if group_number == "all":
        # Получаем индексы моделей для всех групп
        group_model_indexes = []
        for data_array in all_data_arrays:
            group_model_indexes.extend([data["model_index"] for data in data_array])
        logger.info(f"Найдено {len(group_model_indexes)} индексов моделей для всех групп: {group_model_indexes}")
    else:
        # Преобразуем group_number в int, если он не является числом
        if not isinstance(group_number, int):
            try:
                group_number = int(group_number)
            except ValueError:
                logger.error(f"Неверный формат номера группы: {group_number}")
                return ""
        
        # Проверяем корректность номера группы
        if group_number < 1 or group_number > len(all_data_arrays):
            logger.error(f"Некорректный номер группы: {group_number}")
            return ""
        
        data_array = all_data_arrays[group_number - 1]
        logger.info(f"Выбран массив данных для группы {group_number}: {len(data_array)} элементов")

        group_model_indexes = [data["model_index"] for data in data_array]
        logger.info(f"Найдено {len(group_model_indexes)} индексов моделей для группы {group_number}: {group_model_indexes}")

    # Сортируем по увеличению
    group_model_indexes.sort()

    # Преобразуем в строку
    group_model_indexes_str = ", ".join(map(str, group_model_indexes))
    logger.info(f"Результат: {group_model_indexes_str}")
    
    return group_model_indexes_str
