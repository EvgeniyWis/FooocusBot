from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    write_prompt = State()
