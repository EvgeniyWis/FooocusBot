import base64
from .generateData import generateData
from .getFaceSources import *

# Массив дат с нужными параметрами для запроса
dataArray = [generateData("""score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

real_beauty, igbaddie, 1girl, 20 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic blue eyes, long voluminous brown hair, natural skin texture, fine pores, detailed body, subtle highlights

Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
[6.0, 1.6, -0.9, -1.5, 1.5, 1.0, 1.75, 1.0], evanoir_xo_source),

generateData("""score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

    real_beauty, igbaddie, 1girl, 20 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic blue eyes, long voluminous brown hair, natural skin texture, fine pores, detailed body, subtle highlights

    Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
[6.0, 2, -0.9, -1.5, 1.5, 1.0, 1.70, 1.0], face_nika_saintclair_source),

generateData("""score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

real_beauty, igbaddie, 1girl, 20 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic blue eyes, long voluminous brown hair, natural skin texture, fine pores, detailed body, subtle highlights

Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
[6.0, 2.3, -0.9, -1.7, 1.8, 1.0, 1, 0.8], type_chloemay_source),
]

# Функция для прибавления к изначальному промпту каждого элемента массива корневого промпта
def getDataArrayWithRootPrompt(root_prompt: str):
    for data in dataArray:
        data['input']['prompt'] = data['input']['prompt'] + " " + root_prompt

    return dataArray
