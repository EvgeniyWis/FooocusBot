from .setting_1.getDataArray import setting1_getDataArray
from .setting_2.getDataArray import setting2_getDataArray
from .setting_3.getDataArray import setting3_getDataArray
from .setting_4.getDataArray import setting4_getDataArray

# Получение данных для всех настроек
def getAllDataArrays():
    return [
        setting1_getDataArray(),
        setting2_getDataArray(),
        setting3_getDataArray(),
        setting4_getDataArray()
    ]
