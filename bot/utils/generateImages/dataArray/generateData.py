# Глобальная функция для генерации данных для запроса
def generateData(model_name: str, picture_folder_id: str, video_folder_id: str, prompt: str,
    loras: list[dict], base_config_model_name: str, embeddings: list[str] = [], image_number: int = 4):
    data = {"json": {
        "input": {
            "api_name": "txt2img",
            "require_base64": True,
            "prompt": f"{', '.join(embeddings)} {prompt}",
            "loras": loras,
            "image_number": image_number,
            "advanced_params": {"sampler_name": "euler_ancestral", "overwrite_step": 60},
            "negative_prompt": "score_6, score_5, score_4, Negative_&_Positive_Embeddings_By_Stable_Yogi, negative_hand, pony, negativeXL_D, low quality, oversaturated, disfigured, poorly, bad, wrong, mutated, worst quality, normal quality, ugly face, mutated hands, extra fingers, poorly drawn hands, fused fingers, too many fingers, long neck, bad hands, text, signature, signature artist, multiple female, multiple male, bad anatomy, low res, blurry face, blurry eyes, tiny hands, tiny feet, multiple women, disproportionately large head, disproportionately long torso, six fingers, low quality hands, hat, multicolored hair, pubic hair, asian, tan lines, makeup, lipstick, playing cards, black skin, steering wheel, man, naked nipples, naked breasts, cartoon, anime, 3d, cgi, illustration, doll-like, overly muscular, chubby, plastic skin, waxy texture, blurry, jpeg artifacts, extra limbs, distorted proportions, unnatural face, unrealistic anatomy, deformed eyes, exaggerated curves, barbie face, uncanny valley, big head, overexposed, underexposed, low-quality shading, unnatural smile",
            "base_model_name": base_config_model_name,
            "style_selections": [],
            "guidance_scale": 3.5,
            "aspect_ratios_selection": "720*1280"
        }
    }, "model_name": model_name, "picture_folder_id": picture_folder_id, "video_folder_id": video_folder_id}
    return data