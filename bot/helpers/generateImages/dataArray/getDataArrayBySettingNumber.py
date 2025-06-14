from bot.helpers.generateImages.dataArray.setting_1.getDataArray import (
    setting1_getDataArray,
)
from bot.helpers.generateImages.dataArray.setting_2.getDataArray import (
    setting2_getDataArray,
)
from bot.helpers.generateImages.dataArray.setting_3.getDataArray import (
    setting3_getDataArray,
)
from bot.helpers.generateImages.dataArray.setting_4.getDataArray import (
    setting4_getDataArray,
)


def getDataArrayBySettingNumber(setting_number: int):
    if setting_number == 1:
        return setting1_getDataArray()
    elif setting_number == 2:
        return setting2_getDataArray()
    elif setting_number == 3:
        return setting3_getDataArray()
    elif setting_number == 4:
        return setting4_getDataArray()
