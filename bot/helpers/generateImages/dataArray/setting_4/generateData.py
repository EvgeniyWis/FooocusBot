from bot.helpers.generateImages.dataArray.generateData import generateData
from bot.helpers.generateImages.dataArray.setting_4.generateLoras import (
    setting4_generateLoras,
)


# Функция для генерации данных для запроса настройки 4
def setting4_generateData(
    model_name: str,
    picture_folder_id: str,
    video_folder_id: str,
    prompt: str,
    lorasWeights: list[int],
    image_number: int = 4,
    negative_prompt: str = "score_6, score_5, score_4, Negative_&_Positive_Embeddings_By_Stable_Yogi, negative_hand, pony, negativeXL_D, low quality, oversaturated, disfigured, poorly, bad, wrong, mutated, worst quality, normal quality, ugly face, mutated hands, extra fingers, poorly drawn hands, fused fingers, too many fingers, long neck, bad hands, text, signature, signature artist, multiple female, multiple male, bad anatomy, low res, blurry face, blurry eyes, tiny hands, tiny feet, multiple women, disproportionately large head, disproportionately long torso, six fingers, low quality hands, hat, multicolored hair, pubic hair, asian, tan lines, makeup, lipstick, playing cards, black skin, steering wheel, man, naked nipples, naked breasts, cartoon, anime, 3d, cgi, illustration, doll-like, overly muscular, chubby, plastic skin, waxy texture, blurry, jpeg artifacts, extra limbs, distorted proportions, unnatural face, unrealistic anatomy, deformed eyes, exaggerated curves, barbie face, uncanny valley, big head, overexposed, underexposed, low-quality shading, unnatural smile (((ass))), (((butt))), (((buttocks))), (((showing ass)))",
):
    loras = setting4_generateLoras(lorasWeights)
    base_config_model_name = "CyberIllustrious_CyberRealistic.safetensors"
    data = generateData(
        model_name,
        picture_folder_id,
        video_folder_id,
        prompt,
        loras,
        base_config_model_name,
        image_number,
        negative_prompt,
    )
    return data
