from bot.helpers.generateImages.dataArray.extra_setting.generate_data import (
    extra_setting_generate_data,
)

# Функция для генерации массива данных для запроса для экстра-настройки
def extra_setting_get_data_array():
    # Массив дат с нужными параметрами для запроса
    data_array = [
        extra_setting_generate_data(
            "isla_latina",
            "1d7tqTOctKQ6q4uiEGpnbgMwjiZTeiWc3",
            "1d7tqTOctKQ6q4uiEGpnbgMwjiZTeiWc3",
            "",
            [0.55, 1.7, -0.3, 0.75, 0.7, 2.25, 0.05, 0.65]
        ),
    ]

    return data_array
