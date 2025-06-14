# Функция для получения данных из массива объектов по имени модели
async def getDataInDictsArray(array: list[dict], model_name: str):
    result = next(
        (
            ids_dict[model_name]
            for ids_dict in array
            if model_name in ids_dict.keys()
        ),
        None,
    )
    return result
