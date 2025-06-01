from config import SETTING_1_ENDPOINT_ID, SETTING_2_ENDPOINT_ID, SETTING_3_ENDPOINT_ID, SETTING_4_ENDPOINT_ID

# Получение ID эндпоинта для генерации изображений с помощью номера настройки
async def getEndpointID(setting_number: int):
    if setting_number == 1:
        return SETTING_1_ENDPOINT_ID
    elif setting_number == 2:
        return SETTING_2_ENDPOINT_ID
    elif setting_number == 3:
        return SETTING_3_ENDPOINT_ID
    elif setting_number == 4:
        return SETTING_4_ENDPOINT_ID
    else:
        raise Exception(f"Неверный номер настройки: {setting_number}")

