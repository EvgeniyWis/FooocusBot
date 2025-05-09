from .generateLoras import generateLoras
import base64

# Функция для генерации данных для запроса
def generateData(prompt: str, lorasWeights: list[int], image_source: str):
    data = {
        "input": {
            "api_name": "img2img2",
            "require_base64": True,
            "prompt": f"(embedding:Stable_Yogis_PDXL_Positives:1.1), {prompt}",
            "loras": generateLoras(lorasWeights),
            "image_prompts": [
                {
                    "cn_img": base64.b64encode(image_source).decode('utf-8'),
                    "cn_stop": 0.5,
                    "cn_weight": 1,
                    "cn_type": "FaceSwap"
                },
            ],
            "image_number": 4,
            "advanced_params": {"guidance_scale": 3.5, "sampler_name": "euler", "overwrite_step": 30},
            "negative_prompt": "score_6, score_5, score_4, pony, negativeXL_D, low quality, oversaturated, disfigured, poorly, bad, wrong, mutated, worst quality, normal quality, ugly face, mutated hands, extra fingers, poorly drawn hands, fused fingers, too many fingers, long neck, bad hands, text, signature, signature artist, multiple female, multiple male, bad anatomy, mutated hands, low res, blurry face, (hairy pussy:1.2), blurry eyes, tiny hands, tiny feet, multiple women, (((disproportionately large head))), (disproportionately long torso), bad anatomy, six fingers, ((low quality hands)), bad hands, hat, (((multicolored hair))), pubic hair, asian, tan lines, makeup, lipstick, playing cards, black skin, steering wheel, man, naked nipples, (((naked breasts))), (((naked)))"
        }
    }
    return data