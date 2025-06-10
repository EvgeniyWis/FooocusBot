from aiogram.fsm.state import State, StatesGroup

class RandomizerState(StatesGroup):
    write_variable_for_randomizer = State()
    write_value_for_variable_for_randomizer = State()
    write_one_message_for_randomizer = State()