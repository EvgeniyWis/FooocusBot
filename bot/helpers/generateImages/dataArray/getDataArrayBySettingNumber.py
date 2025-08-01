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


def getDataArrayBySettingNumber(setting_number: str | int):
    # Если передана строка, преобразуем её в число
    if isinstance(setting_number, str):
        if setting_number.isdigit():
            setting_number = int(setting_number)

    if setting_number == 1:
        return setting1_get_data_array()
    elif setting_number == 2:
        return setting2_get_data_array()
    elif setting_number == 3:
        return setting3_get_data_array()
    elif setting_number == 4:
        return setting4_get_data_array()
    elif setting_number == "extra":
        return extra_group_get_data_array()

    raise ValueError(f"Неизвестный номер настройки: {setting_number}")