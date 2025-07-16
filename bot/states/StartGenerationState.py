from aiogram.fsm.state import State, StatesGroup


class StartGenerationState(StatesGroup):
    write_prompt_for_images = State()
    write_prompt_for_video = State()
    write_prompt_for_quick_video_generation = State()
    write_prompt_for_model = State()
    send_image_for_video_generation = State()
    write_prompt_for_img2video = State()
    ask_for_model_index_for_img2video = State()
    write_new_prompt_for_regenerate_image = State()
    write_prompt_for_nsfw_generation = State()
    ask_video_length_input = State()
    choose_generated_video = State()
    write_multi_prompts_for_models = State()
    write_models_for_specific_generation = State()


class MultiPromptInputState(StatesGroup):
    collecting_prompt_parts = State()
    collecting_model_prompts_for_settings = State()


class UserLoraEditStates(StatesGroup):
    waiting_for_weight_input = State()
    waiting_for_lora_to_add = State()
    selected_setting_number = State()
    selected_lora_title = State()


class LoraEditStates(StatesGroup):
    waiting_for_new_title = State()
    waiting_for_add_title = State()
    selected_setting_number = State()


class ModelEditStates(StatesGroup):
    waiting_for_model_name = State()
    waiting_for_model_rename = State()
    selected_setting_number = State()
    old_model_name = State()


class UserPromptWrite(StatesGroup):
    waiting_for_prompt_input = State()
