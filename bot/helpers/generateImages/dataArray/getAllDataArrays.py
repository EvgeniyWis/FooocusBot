from bot.helpers.generateImages.dataArray.settings.setting_1.get_data_array import (
    setting1_get_data_array,
)
from bot.helpers.generateImages.dataArray.settings.setting_2.get_data_array import (
    setting2_get_data_array,
)
from bot.helpers.generateImages.dataArray.settings.setting_3.get_data_array import (
    setting3_get_data_array,
)
from bot.helpers.generateImages.dataArray.settings.setting_4.get_data_array import (
    setting4_get_data_array,
)
from bot.helpers.generateImages.dataArray.extra_setting.get_data_array import (
    extra_group_get_data_array,
)


# Получение данных для всех настроек
def getAllDataArrays():
    return [
        setting1_get_data_array(),
        setting2_get_data_array(),
        setting3_get_data_array(),
        setting4_get_data_array(),
        extra_group_get_data_array(),
    ]
