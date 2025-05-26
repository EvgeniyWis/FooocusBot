from aiogram.fsm.context import FSMContext

# Функция для увеличения count даты в стейте
async def increaseCountInState(state: FSMContext, key: str, amount: int = 1):
    stateData = await state.get_data()
    stateData[key] += amount
    await state.update_data(saved_images_count=stateData[key])