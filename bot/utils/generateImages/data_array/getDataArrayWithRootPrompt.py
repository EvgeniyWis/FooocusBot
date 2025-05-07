import base64
from .getFaceSources import *
from .generateLoras import generateLoras

# Массив дат с нужными параметрами для запроса
dataArray = [{
        "input": {
            "api_name": "img2img2",
            "require_base64": True,
            "prompt": """embedding:Stable_Yogis_PDXL_Positives, score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

real_beauty, igbaddie, 1girl, 20 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic blue eyes, long voluminous brown hair, natural skin texture, fine pores, detailed body, subtle highlights

Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
            "loras": generateLoras([6.0, 1.6, -0.9, -1.5, 1.5, 1.0, 1.75, 1.0]),
            "image_prompts": [
                {
                    "cn_img": base64.b64encode(evanoir_xo_source).decode('utf-8'),
                    "cn_stop": 0.5,
                    "cn_weight": 1,
                    "cn_type": "FaceSwap"
                },
            ],
            "advanced_params": {"adaptive_cfg": 3.5, "sampler_name": "Euler", "overwrite_step": 30},
            "negative_prompt": "score_6, score_5, score_4, pony, negativeXL_D, low quality, oversaturated, disfigured, poorly, bad, wrong, mutated, worst quality, normal quality, ugly face, mutated hands, extra fingers, poorly drawn hands, fused fingers, too many fingers, long neck, bad hands, text, signature, signature artist, multiple female, multiple male, bad anatomy, mutated hands, low res, blurry face, (hairy pussy:1.2), blurry eyes, tiny hands, tiny feet, multiple women, (((disproportionately large head))), (disproportionately long torso), bad anatomy, six fingers, ((low quality hands)), bad hands, hat, (((multicolored hair))), pubic hair, asian, tan lines, makeup, lipstick, playing cards, black skin, steering wheel, man, naked nipples, (((naked breasts))), (((naked)))"
        }
    },
    {
            "input": {
                "api_name": "img2img2",
                "require_base64": True,
                "prompt": """embedding:Stable_Yogis_PDXL_Positives, score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

    real_beauty, igbaddie, 1girl, 20 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic blue eyes, long voluminous brown hair, natural skin texture, fine pores, detailed body, subtle highlights

    Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
                "loras": generateLoras([6.0, 2, -0.9, -1.5, 1.5, 1.0, 1.70, 1.0]), 
                "image_prompts": [
                    {
                        "cn_img": base64.b64encode(face_nika_saintclair_source).decode('utf-8'),
                        "cn_stop": 0.5,
                        "cn_weight": 1,
                        "cn_type": "FaceSwap"
                    },
                ],
                "advanced_params": {"adaptive_cfg": 3.5, "sampler_name": "Euler", "overwrite_step": 30},
                "negative_prompt": "score_6, score_5, score_4, pony, negativeXL_D, low quality, oversaturated, disfigured, poorly, bad, wrong, mutated, worst quality, normal quality, ugly face, mutated hands, extra fingers, poorly drawn hands, fused fingers, too many fingers, long neck, bad hands, text, signature, signature artist, multiple female, multiple male, bad anatomy, mutated hands, low res, blurry face, (hairy pussy:1.2), blurry eyes, tiny hands, tiny feet, multiple women, (((disproportionately large head))), (disproportionately long torso), bad anatomy, six fingers, ((low quality hands)), bad hands, hat, (((multicolored hair))), pubic hair, asian, tan lines, makeup, lipstick, playing cards, black skin, steering wheel, man, naked nipples, (((naked breasts))), (((naked)))"
            }
        },
    {
            "input": {
                "api_name": "img2img2",
                "require_base64": True,
                "prompt": """embedding:Stable_Yogis_PDXL_Positives, score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

real_beauty, igbaddie, 1girl, 20 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic blue eyes, long voluminous brown hair, natural skin texture, fine pores, detailed body, subtle highlights

Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
                "loras": generateLoras([6.0, 2.3, -0.9, -1.7, 1.8, 1.0, 1, 0.8]),
                "image_prompts": [
                    {
                        "cn_img": base64.b64encode(type_chloemay_source).decode('utf-8'),
                        "cn_stop": 0.5,
                        "cn_weight": 1,
                        "cn_type": "FaceSwap"
                    },
                ],
                "advanced_params": {"adaptive_cfg": 3.5, "sampler_name": "Euler", "overwrite_step": 30},
                "negative_prompt": "score_6, score_5, score_4, pony, negativeXL_D, low quality, oversaturated, disfigured, poorly, bad, wrong, mutated, worst quality, normal quality, ugly face, mutated hands, extra fingers, poorly drawn hands, fused fingers, too many fingers, long neck, bad hands, text, signature, signature artist, multiple female, multiple male, bad anatomy, mutated hands, low res, blurry face, (hairy pussy:1.2), blurry eyes, tiny hands, tiny feet, multiple women, (((disproportionately large head))), (disproportionately long torso), bad anatomy, six fingers, ((low quality hands)), bad hands, hat, (((multicolored hair))), pubic hair, asian, tan lines, makeup, lipstick, playing cards, black skin, steering wheel, man, naked nipples, (((naked breasts))), (((naked)))"
            }
        }
]

# Функция для прибавления к изначальному промпту каждого элемента массива корневого промпта
def getDataArrayWithRootPrompt(root_prompt: str):
    for data in dataArray:
        data['input']['prompt'] = data['input']['prompt'] + " " + root_prompt

    return dataArray
