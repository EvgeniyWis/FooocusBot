from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Инлайн-клавиатура для выбора количества генераций
def generationsAmountKeyboard(dataArrayLen: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙️ Тестовая генерация - 1', callback_data='generations_amount|test')],
    [InlineKeyboardButton(text=f'⚡️ Рабочая генерация - {dataArrayLen}', callback_data='generations_amount|all')]])

    return kb