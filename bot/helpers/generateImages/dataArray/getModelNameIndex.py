from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)


def getModelNameIndex(model_name: str):
    # Убираем +N, если он есть (например: "1+1" → "1")
    model_name = model_name.split("+")[0]

    # Получаем все группы
    all_groups = getAllDataArrays()

    # Ищем, в какой группе находится модель с таким названием
    for index, group in enumerate(all_groups):
        for dataArray in group:
            if dataArray["model_name"] == model_name:
                if index == 0:
                    return group.index(dataArray) + 1
                else:
                    return (
                        sum(len(group) for group in all_groups[:index])
                        + group.index(dataArray)
                        + 1
                    )

    return None
