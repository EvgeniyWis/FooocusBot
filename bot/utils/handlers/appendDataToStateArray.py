from aiogram.fsm.context import FSMContext

from bot.logger import logger


async def appendDataToStateArray(
    state: FSMContext,
    key: str,
    value: dict,
    unique_keys=("model_name", "image_index"),
):
    state_data = await state.get_data()
    data_list = state_data.get(key, [])
    updated = False
    for idx, item in enumerate(data_list):
        if all(item.get(k) == value.get(k) for k in unique_keys):
            data_list[idx] = value
            updated = True
            break
    if unique_keys is None:
        data_list.append(value)
        await state.update_data(**{key: data_list})
        return
    if not updated:
        data_list.append(value)

    await state.update_data(**{key: data_list})
