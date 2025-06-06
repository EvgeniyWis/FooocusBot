from aiogram.fsm.context import FSMContext
from typing import Any


# Функция для добавления данных в массив в стейте
async def appendDataToStateArray(state: FSMContext, key: str, value: Any):
    stateData = await state.get_data()
    if key not in stateData:
        await state.update_data(**{key: [value]})
    else:
        # Добавляем в стейт путь к изображению для faceswap
        stateData[key].append(value)
        await state.update_data(**{key: stateData[key]})

