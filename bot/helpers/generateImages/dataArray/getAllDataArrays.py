import asyncio

from bot.helpers.generateImages.dataArray.extra_setting.get_data_array import (
    extra_setting_get_data_array,
)
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


# Получение данных для всех настроек
async def getAllDataArrays(user_id: int):
    return await asyncio.gather(
        setting1_get_data_array(user_id),
        setting2_get_data_array(),
        setting3_get_data_array(),
        setting4_get_data_array(),
        extra_setting_get_data_array(),
    )
