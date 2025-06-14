from typing import Any

from aiogram.fsm.context import FSMContext


# Функция для добавления данных в массив в стейте
async def appendDataToStateArray(state: FSMContext, key: str, value: Any):
    state_data = await state.get_data()
    if key not in state_data:
        await state.update_data(**{key: [value]})
    else:
        # Добавляем в стейт путь к изображению для faceswap
        data = state_data.get(key, [])
        data.append(value)
        await state.update_data(**{key: data})
