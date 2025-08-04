from bot.helpers.generateImages.dataArray.groups.extra_group.get_data_array import (
    extra_group_get_data_array,
)
from bot.helpers.generateImages.dataArray.groups.first_group.get_data_array import (
    first_group_get_data_array,
)
from bot.helpers.generateImages.dataArray.groups.second_group.get_data_array import (
    second_group_get_data_array,
)


# Получение данных для всех настроек
def getAllDataArrays():
    return [
        first_group_get_data_array(),
        second_group_get_data_array(),
        extra_group_get_data_array(),
    ]
