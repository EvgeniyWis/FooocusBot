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
    write_prompt_for_video_generation_by_one_prompt = State()
    # Новые состояния для img2video с уникальными промптами
    write_multi_prompts_for_img2video = State()
    collecting_prompt_parts_for_img2video = State()
    # Состояние для старого функционала одного промпта в img2video
    write_single_prompt_for_img2video = State()


class MultiPromptInputState(StatesGroup):
    collecting_prompt_parts = State()
    collecting_model_prompts_for_groups = State()
