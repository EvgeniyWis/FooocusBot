from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    write_prompt_for_image = State()
    write_prompt_for_video = State()
