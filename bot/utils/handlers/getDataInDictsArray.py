# Функция для получения данных из массива объектов по имени модели и индексу изображения
async def getDataInDictsArray(
    array: list[dict],
    model_name: str,
    image_index: int = None,
    video_index: int = None,
):
    if isinstance(array, dict):  # fallback
        return array.get(model_name)

    for item in array:
        if not isinstance(item, dict):
            continue

        if video_index is not None:
            if (
                item.get("model_name") == model_name
                and item.get("image_index") == image_index
                and item.get("video_index") == video_index
            ):
                return item.get("direct_url")

        if image_index is not None:
            if (
                item.get("model_name") == model_name
                and item.get("image_index") == image_index
            ):
                return item.get("direct_url")
        elif item.get("model_name") == model_name:
            return item.get("prompt")
        elif model_name in item:
            return item[model_name]

    return None
