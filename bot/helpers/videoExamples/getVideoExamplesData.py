from bot.config import DEVELOPMENT_MODE


# Функция для получения примеров шаблонов для генерации видео с помощью kling
async def getVideoExamplesData() -> dict:
    # Формируем массив из промптов
    prompts = [
        "Her hips move vigorously and powerfully from side to side in a single horizontal plane, with wide and dynamic amplitude, creating strong, expressive motion entirely focused in the lower body.Her arms are placed behind her back, with wrists not visible in the frame.Her upper body stays stable and composed, highlighting the contrast between the intense hip motion and the stillness above.The focus is on the powerful, energetic hip movement contrasted with the static upper body and concealed arm position.Eyes open, soft smile with lips closed, slight head tilt.",
        "The woman performs an energetic, sensual dance with her legs confidently spread apart. Her hips snap and sway in wide, rhythmic motions, while her torso and chest roll with bold, expressive movement. Her hands stay in place. She maintains a teasing, seductive smile and an inviting gaze. The camera stays fixed, capturing her full-body motion under soft, warm lighting, emphasizing the power and fluidity of her performance.",
        "The woman performs an energetic, sensual dance with her legs confidently spread apart. Her hips snap and sway in wide, rhythmic motions, while her torso and chest roll with bold, expressive movement. Her hands stay in place. She maintains a teasing, seductive smile and an inviting gaze. The camera stays fixed, capturing her full-body motion under soft, warm lighting, emphasizing the power and fluidity of her performance.",
        "The woman, with eyes open and a calm, confident facial expression, moves to sit on the counter. She places herself securely on the surface and lifts both legs, placing her feet up onto the counter as well. Her hands are placed firmly on the counter, supporting her body weight, ensuring stability and balance. She maintains a composed and steady posture. The camera remains static, capturing the smooth and controlled movement. Lighting is soft and natural, with a warm tone. The focus is on the natural transition to the seated position and the steady, grounded body posture.",
        "In a softly lit room with natural light spilling through large windows, the atmosphere feels relaxed and intimate. The subject, exuding effortless charm, slightly smiles as she begins to play with her hair, creating a sense of allure. She shifts her shoulders gracefully from left to right, her movements light and playful, giving an almost dance-like quality. The camera draws closer, catching the glint of mischief in her eyes.The subject slowly leans forward toward the lens, a teasing glimmer in her expression. As she leans in, she gives a gentle smooch towards the camera, the sound soft yet inviting, as if sharing a secret with the viewer. Her chest subtly moves with the rhythm of her movements, adding to the charm of the moment.With a playful wink, she pulls back slightly, a warm smile spreading across her face, leaving a lingering sense of connection that invites the viewer into her world.",
        "Eyes open, soft smile with lips closed, slight head tilt. Hips move actively in a rhythmic, fluid motion, creating an energetic and dynamic dance, with the movement focused on the waist and lower body. Hands firmly resting on her waist, staying still and in place. Posture is confident and relaxed, expression calm and natural, maintaining a controlled and lively dance. Close-up shot, soft, natural lighting with balanced warmth, ensuring no overexposure.",
    ]

    # Формируем массив из file_id видео
    if DEVELOPMENT_MODE:
        video_ids = [
            "BAACAgIAAxkBAAK3nWgyCpXl79L5peVJ5dnsGnmozlvVAAINawACP6tQSZWtaZ9qiyFCNgQ",
            "BAACAgIAAxkBAAK3nmgyCpX48oVWcv9CR5478XLG2OXCAAIQawACP6tQSX0FEkOg-TfRNgQ",
            "BAACAgIAAxkBAAK3oGgyCpV6vQW9r7ox2AfiAAHp-18XiAACDmsAAj-rUEleOThVyLTJPjYE",
            "BAACAgIAAxkBAAK3oWgyCpVZuhCRPFaVq5QeQp6TRh7OAAIocAACihNRSWVwUNXKu2cbNgQ",
            "BAACAgIAAxkBAAK3n2gyCpVz_IvRxDlcV8BZ0EGWQlIiAAIPawACP6tQSciFMwnTz-roNgQ",
            "BAACAgIAAxkBAAK3omgyCpU3DRy7cRMowbxGWB4x4J6EAAIvcAACihNRScLPI7SUpqb2NgQ",
        ]
    else:
        video_ids = [
            "BAACAgIAAxkBAAPraCmALgLMyj3hYfhAZxMcUu_xNBIAAg1rAAI_q1BJH4l_Wztt8bg2BA",
            "BAACAgIAAxkBAAPuaCmALgPZpRy-MD_wDhnchrOWV2cAAhBrAAI_q1BJ0GEn22fOOnA2BA",
            "BAACAgIAAxkBAAPtaCmALtvwc4-Sp_7FPBBjyqqLfXoAAg9rAAI_q1BJRM5-AAETncrMNgQ",
            "BAACAgIAAxkBAAPsaCmALqx-5jWYl6G2gjf5Y4HuvBoAAg5rAAI_q1BJ_6h6PvF9cqE2BA",
            "BAACAgIAAxkBAAID1GgpwxspBCUUICk5wBxEfyMOvcHAAAIocAACihNRSZ3p6zpuo9SgNgQ",
            "BAACAgIAAxkBAAID1mgpw1gqEtclVWECyTUzoVml2TxMAAIvcAACihNRSZ3p6zpuo9SgNgQ",
        ]
    # Если длина массива промптов и длина массива видео не равны, то выводим ошибку
    if len(prompts) != len(video_ids):
        raise ValueError(
            "Длина массива промптов и длина массива видео не равны"
        )

    # Формируем объект с промптами и видео
    result = {}
    for index, video_id in enumerate(video_ids):
        result[index] = {"file_id": video_id, "prompt": prompts[index]}

    return result
