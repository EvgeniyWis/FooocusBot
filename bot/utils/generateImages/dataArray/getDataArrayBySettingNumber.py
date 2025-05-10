from .setting_1.getDataArray import setting1_getDataArray

def getDataArrayBySettingNumber(setting_number: int):
    if setting_number == 1:
        return setting1_getDataArray()
