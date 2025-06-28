# Функция для получения данных из массива объектов по имени модели и индексу изображения
async def getDataInDictsArray(
    array: list[dict], model_name: str, image_index: int = None
):
    for item in array:
        if not isinstance(item, dict):
            continue

        # Если передан image_index, ищем по обоим параметрам
        if image_index is not None:
            if (
                item.get("model_name") == model_name
                and item.get("image_index") == image_index
            ):
                return item.get("direct_url")
        # Иначе ищем только по model_name (обратная совместимость)
        elif model_name in item:
            return item[model_name]

    return None
