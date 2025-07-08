from aiogram.fsm.state import State, StatesGroup


class StartGenerationState(StatesGroup):
    write_prompt_for_images = State()
    write_prompt_for_video = State()
    write_prompt_for_quick_video_generation = State()
    write_prompt_for_model = State()
    write_model_name_for_generation = State()
    send_image_for_video_generation = State()
    write_prompt_for_img2video = State()
    ask_for_model_name_for_video_generation_from_image = State()
    write_new_prompt_for_regenerate_image = State()
    write_prompt_for_nsfw_generation = State()
    ask_video_length_input = State()
    choose_generated_video = State()
    write_multi_prompts_for_models = State()
