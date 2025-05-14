from .generateLoras import setting1_generateLoras
from ..generateData import generateData

# Функция для генерации данных для запроса настройки 1
def setting1_generateData(model_name: str, picture_folder_id: str, video_folder_id: str, prompt: str, lorasWeights: list[int]):
    loras = setting1_generateLoras(lorasWeights)
    embeddings = ["(embedding:Negative_&_Positive_Embeddings_By_Stable_Yogi:1.1)"]
    advanced_params = {"guidance_scale": 3.5, "sampler_name": "euler", "overwrite_step": 30}
    negative_prompt = "score_6, score_5, score_4, pony, negativeXL_D, low quality, oversaturated, disfigured, poorly, bad, wrong, mutated, worst quality, normal quality, ugly face, mutated hands, extra fingers, poorly drawn hands, fused fingers, too many fingers, long neck, bad hands, text, signature, signature artist, multiple female, multiple male, bad anatomy, mutated hands, low res, blurry face, (hairy pussy:1.2), blurry eyes, tiny hands, tiny feet, multiple women, (((disproportionately large head))), (disproportionately long torso), bad anatomy, six fingers, ((low quality hands)), bad hands, hat, (((multicolored hair))), pubic hair, asian, tan lines, makeup, lipstick, playing cards, black skin, steering wheel, man, naked nipples, (((naked breasts))), (((naked)))"
    base_config_model_name = "CyberRealistic_Pony.safetensors"
    data = generateData(model_name, picture_folder_id, video_folder_id, prompt, loras, advanced_params, base_config_model_name, negative_prompt, embeddings)
    return data