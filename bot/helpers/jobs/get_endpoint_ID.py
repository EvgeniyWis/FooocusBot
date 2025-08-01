from bot.settings import settings


# Получение ID эндпоинта для генерации изображений с помощью номера настройки
async def get_endpoint_ID(group_number: str | int):
    # Если передана строка, преобразуем её в число
    if isinstance(group_number, str):
        if group_number.isdigit():
            group_number = int(group_number)

    match group_number:
        case 1:
            return settings.SETTING_1_ENDPOINT_ID
        case 2:
            return settings.SETTING_2_ENDPOINT_ID
        case 3:
            return settings.SETTING_3_ENDPOINT_ID
        case 4:
            return settings.SETTING_4_ENDPOINT_ID
        case "extra":
            return settings.EXTRA_SETTING_ENDPOINT_ID
        case _:
            raise Exception(f"Неверный номер настройки: {group_number}")
