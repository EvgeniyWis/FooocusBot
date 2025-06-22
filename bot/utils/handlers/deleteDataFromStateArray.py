from aiogram.fsm.context import FSMContext


async def deleteDataFromStateArray(state: FSMContext, key: str, value: str, value_key: str):
    """
    Удаляет данные из массива в стейте по ключу и имени модели

    Attributes:
        state (FSMContext): контекст состояния
        key (str): ключ массива
        value (str): значение, по которому будет идентифироваться данные для удаления
        value_key (str): ключ значения, по которому будет идентифироваться данные для удаления
    Returns:
        None
    """
    state_data = await state.get_data()
    data = state_data.get(key, [])
    for item in data:
        if item[value_key] == value:
            data.remove(item)
    await state.update_data(**{key: data})

