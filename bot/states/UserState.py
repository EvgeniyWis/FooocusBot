from aiogram.fsm.state import State, StatesGroup

class StartGenerationState(StatesGroup):
    write_prompt_for_images = State()
    write_prompt_for_video = State()
    write_prompt_for_model = State()

class RandomizerState(StatesGroup):
    write_variable_for_randomizer = State()
    write_value_for_variable_for_randomizer = State()
    write_prompt_for_randomizer = State()