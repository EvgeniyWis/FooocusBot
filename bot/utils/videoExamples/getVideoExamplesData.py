import os

# Функция для получения примеров шаблонов для генерации видео с помощью kling
async def getVideoExamplesData() -> dict:
    # Путь к папке с видео
    folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "videos", "templates_examples")
    
    # Расширения видеофайлов, которые хотим найти
    video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"}

    # Получаем список всех файлов в папке с нужными расширениями
    video_files = [f for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f)) and
                os.path.splitext(f)[1].lower() in video_extensions]

    # Формируем массив из промптов
    prompts = [
    "Her hips move vigorously and powerfully from side to side in a single horizontal plane, with wide and dynamic amplitude, creating strong, expressive motion entirely focused in the lower body.Her arms are placed behind her back, with wrists not visible in the frame.Her upper body stays stable and composed, highlighting the contrast between the intense hip motion and the stillness above.The focus is on the powerful, energetic hip movement contrasted with the static upper body and concealed arm position.Eyes open, soft smile with lips closed, slight head tilt.", 
    "The woman, with eyes open and a calm, confident facial expression, moves to sit on the counter. She places herself securely on the surface and lifts both legs, placing her feet up onto the counter as well. Her hands are placed firmly on the counter, supporting her body weight, ensuring stability and balance. She maintains a composed and steady posture. The camera remains static, capturing the smooth and controlled movement. Lighting is soft and natural, with a warm tone. The focus is on the natural transition to the seated position and the steady, grounded body posture.", 
    "The woman performs an energetic, sensual dance with her legs confidently spread apart. Her hips snap and sway in wide, rhythmic motions, while her torso and chest roll with bold, expressive movement. Her hands stay in place. She maintains a teasing, seductive smile and an inviting gaze. The camera stays fixed, capturing her full-body motion under soft, warm lighting, emphasizing the power and fluidity of her performance.",
    "The woman performs an energetic, sensual dance with her legs confidently spread apart. Her hips snap and sway in wide, rhythmic motions, while her torso and chest roll with bold, expressive movement. Her hands stay in place. She maintains a teasing, seductive smile and an inviting gaze. The camera stays fixed, capturing her full-body motion under soft, warm lighting, emphasizing the power and fluidity of her performance."]

    # Если длина массива промптов и длина массива видео не равны, то выводим ошибку
    if len(prompts) != len(video_files):
        raise ValueError("Длина массива промптов и длина массива видео не равны")

    # Формируем объект с промптами и видео
    result = {}
    for index, file in enumerate(video_files):
        result[index] = {"file_path": os.path.join(folder_path, file), "prompt": prompts[index]}

    return result