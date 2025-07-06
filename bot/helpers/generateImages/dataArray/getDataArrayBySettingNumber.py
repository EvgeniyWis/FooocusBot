from bot.helpers.generateImages.dataArray.setting_1.get_data_array import (
    setting1_get_data_array,
)
from bot.helpers.generateImages.dataArray.setting_2.get_data_array import (
    setting2_get_data_array,
)
from bot.helpers.generateImages.dataArray.setting_3.get_data_array import (
    setting3_get_data_array,
)
from bot.helpers.generateImages.dataArray.setting_4.get_data_array import (
    setting4_get_data_array,
)
from bot.helpers.generateImages.dataArray.extra_setting.get_data_array import (
    extra_setting_get_data_array,
)


def getDataArrayBySettingNumber(setting_number: str | int):
    if setting_number == 1:
        return setting1_get_data_array()
    elif setting_number == 2:
        return setting2_get_data_array()
    elif setting_number == 3:
        return setting3_get_data_array()
    elif setting_number == 4:
        return setting4_get_data_array()
    elif setting_number == "extra":
        return extra_setting_get_data_array()
