# Текст для стартового меню
START_TEXT = """
👋 Welcome to the image generation bot!
To get started, choose the type of generation you will use:

⚡️ Production generation — used for generating production images; it is not recommended to run multiple generations in parallel.
"""

# Текст при отсутствии доступа
ACCESS_DENIED_TEXT = (
    "❌ You do not have access to this bot! Please contact the developer."
)

# Текст при успешном выборе групп
GET_GROUPS_SUCCESS_TEXT = (
    "✅ Groups selected successfully! Now type your prompt:"
)

# Текст при получении промпта
GET_PROMPT_SUCCESS_TEXT = (
    "Submitting requests to generate images..."
)

# Текст после выбора количества генераций
GET_GENERATIONS_SUCCESS_TEXT = """
✅ Generation type selected successfully!
‼️ When you press one of the buttons below, data from the previous generation will be completely cleared!
Now choose which group you will use:
"""

# Текст при выборе одного промпта для всех изображений
GET_ONE_PROMPT_GENERATION_SUCCESS_TEXT = (
    "✅ Selection processed successfully! Now choose the prompt writing mode:"
)

EMPTY_MATCHES_WRITE_PROMPTS_TEXT = """
❗️ No prompts were found for your request! Please check the spelling:
Model number - prompt
Model number - prompt

Example:
1 - prompt
2 - prompt
"""

WRITE_PROMPTS_FOR_MODELS_TEXT = """
✍️ Write a list of prompts by model in the format:\n\n
Model number - prompt
Model number - prompt

Example:
1 - prompt
2 - prompt

⚠️ Use only indexes that belong to this group:
{}

When you finish entering the prompts in this message press the "✅ Done" button
"""


# Текст при выборе режима статичного промпта
GET_STATIC_PROMPT_TYPE_SUCCESS_TEXT = (
    "✅ Selection processed successfully! Now enter your prompt:"
)

# Текст при выборе группы и рабочей генерации для выбора режима написания промпта
CHOOSE_WRITE_PROMPT_TYPE_SUCCESS_TEXT = (
    "✅ Selection processed successfully! Now choose the prompt writing mode:"
)

# Текст при выборе режима написания промпта
GET_WRITE_PROMPT_TYPE_SUCCESS_TEXT = "✅ The selected prompt writing mode will now be used! Now enter your prompt:"

# Текст для старта написания уникального промпта для конкретной модели
WRITE_PROMPT_FOR_MODEL_START_TEXT = "✅ Okay, let's begin. Enter your prompt for model {} with number {}:"

# Текст для готовности написания уникального промпта для конкретной модели
WRITE_PROMPT_FOR_MODEL_TEXT = "Press the button below when you're ready to enter the prompt for the next model {} with number {}:"

# Текст для написания уникального промпта для конкретной модели
WRITE_UNIQUE_PROMPT_FOR_MODEL_TEXT = (
    "✅ Enter your prompt for model {} with number {}:"
)

# Текст при получении id работы для одной модели
GENERATE_IMAGES_PROCESS_TEXT = """
✅ Success: {}
❌ Error: {}
🚫 Canceled: {}
⚡️ In progress: {}
⏳ In queue: {}
🔄 Remaining: {}

🖼 Generating images...
"""

# Текст при получении id работы для множества моделей
GENERATE_IMAGES_PROCESS_TEXT_FOR_MANY_MODELS = """
✅ Success: {}
❌ Error: {}
🚫 Canceled: {}
⚡️ In progress: {}
⏳ In queue: {}
🔄 Remaining: {}

🖼 Generating images...

❗️ When generation succeeds, press the buttons under the models with a short delay; otherwise errors may occur.
"""

# Текст при ошибке генерации
GENERATION_IMAGE_ERROR_TEXT = (
    "An error occurred while generating the image! \nError text: \n<code>{}</code>"
)

# Текст при отправке изображений и выбора одного из них
SELECT_IMAGE_TEXT = "☝️ Select one of the images (the first image is the reference) that best matches your prompt for model {} with number {}:"

SELECT_SOME_IMAGES_TEXT = "☝️Select the images (the first image is the reference) that best match your prompt for model {} with number {}: \nPress the buttons with a short delay; otherwise errors may occur."

# Текст при замене лица на изображении
FACE_SWAP_PROGRESS_TEXT = "🔄 Replacing the face on the selected image {} for model {} with number {}..."

# Текст при ошибке замены лица
FACE_SWAP_ERROR_TEXT = "Failed to perform face swap for model {} with number {}! Please try again. \nError text: <code>{}</code>"

# Текст пока модель ждёт своей очереди на замену лица
FACE_SWAP_WAIT_TEXT = "🔄 The selected image {} for model {} with number {} is waiting its turn for face swap..."

# Текст при ошибке сохранения изображения
SAVE_FILE_ERROR_TEXT = "Failed to save the file for model {} with number {}! Please try again."

# Текст при сохранении изображения
SAVE_IMAGE_PROGRESS_TEXT = (
    "🔄 Saving image for model {} with number {}..."
)

# Текст при успешной замене лица
FACE_SWAP_SUCCESS_TEXT = (
    "✅ Face successfully swapped! \nModel name: {} \nModel number: {}"
)

# Текст при отправке изображения для его сохранения
START_SAVE_IMAGE_TEXT = "Choose an action for the final image together with the reference photo for model {} with number {}:"

# Текст при успешном сохранении изображений
SAVE_IMAGES_SUCCESS_TEXT = """
✅ The image has been successfully saved to the folder and is available at this link:
{}
Model name: {}
Model folder link: {}
Model number: {}
"""

# Текст при успешном сохранении изображений с использованием Magnific Upscaler
SAVE_IMAGES_SUCCESS_TEXT_WITH_MAGNIFIC_UPSCALER = """
✅🪄 The image using Magnific Upscaler has been successfully saved to the folder and is available at this link:
{}
Model name: {}
Model folder link: {}
Model number: {}
"""

# Текст при успешном сохранении видео
SAVE_VIDEO_SUCCESS_TEXT = """
✅ The video has been successfully saved to the folder and is available at this link:
{}
Model name: {}
Model folder link: {}
Model number: {}
"""

# Текст при нажатии на кнопку "✒️ Написать свой промпт"
WRITE_PROMPT_FOR_VIDEO_TEXT = "✒️ Write your prompt by which a video will be generated for model {} with number {}:"

WRITE_PROMPT_FOR_NSFW_VIDEO_TEXT = """
⏳ Please note that generating NSFW video can take a long time.

✒️ Write your prompt by which an NSFW video will be generated for model {} with number {}

<b>Recommended quality prompt:</b>
<code>
A naked girl strokes her bare breasts with her hands, sensual movement, static camera, cinematic lighting, natural body physics, 4K detail, eye contact
</code>
"""

# Текст при написании кастомного промпта для видео
WRITE_PROMPT_FOR_VIDEO_SUCCESS_TEXT = "✅ The prompt for model {} with number {} has been received! \nNow choose the type of video generation:"

# Текст при успешной генерации видео
GENERATE_VIDEO_SUCCESS_TEXT = """
✅ Video successfully generated!
Model name: {}
Model number: {}
"""

# Текст при генерации видео
GENERATE_VIDEO_PROGRESS_TEXT = (
    "🔄 Generating video for model {} with number {}..."
)

# Текст при сохранении видео
SAVE_VIDEO_PROGRESS_TEXT = "🔄 Saving video for model {} with number {}..."

# Текст при ошибке генерации видео
GENERATE_VIDEO_ERROR_TEXT = "An error occurred while generating the video for model {} with number {}! \nError text: <code>{}</code>"

# Текст при ошибке генерации видео из изображения
GENERATE_VIDEO_FROM_IMAGE_ERROR_TEXT = "An error occurred while generating the video! \nError text: <code>{}</code>"

# Текст при генерации изображений
GENERATE_IMAGE_PROGRESS_TEXT = (
    "🔄 Generating images for model {} with number {}..."
)

# Текст при upscale изображения
UPSCALE_IMAGE_PROGRESS_TEXT = (
    "🔄 Upscaling image {} for model {} with number {}..."
)

# Текст при втором upscale изображения с помощью ILoveAPI
SECOND_UPSCALE_IMAGE_PROGRESS_TEXT = (
    "🔄 Performing second upscale for image {} for model {} with number {} using ILoveAPI..."
)

# Текст об обработке выбора изображения
SELECT_IMAGE_PROGRESS_TEXT = "🔄 Processing image selection..."

# Текст при остановке генерации
STOP_GENERATION_TEXT = "Generation stopped! 🚫"

# Текст при останавливании генерации
STOP_GENERATION_TEXT_WITH_WAITING = (
    "Generation is stopping... \nPlease wait..."
)

# Текст при перегенерации изображения
REGENERATE_IMAGE_TEXT = (
    "🔄 Regenerating images for model {} with number {}..."
)

# Текст при перегенерации изображения с новым промптом
REGENERATE_IMAGE_WITH_NEW_PROMPT_TEXT = "🔄 Regenerating images for model {} with number {} with a new prompt: \n{}"

# Текст при выборе режима рандомайзера
GET_RANDOM_PROMPT_TYPE_SUCCESS_TEXT = "✅ Randomizer selected successfully! \nNow you can add variables and their values to the randomizer using this menu:"

# Текст при вводе переменной для рандомайзера
WRITE_VARIABLE_FOR_RANDOMIZER_TEXT = "✅ You have successfully entered the name of your prompt variable! \nNow enter values for this variable and when you are finished, just press the button below:"

# Если выбрана кнопка "✅ Добавить переменную"
ADD_VARIABLE_FOR_RANDOMIZER_TEXT = (
    "✅ Enter the name of the prompt variable:"
)

# Текст в меню рандомайзера
RANDOMIZER_MENU_TEXT = "⚙️ In the randomizer menu, you can add and change variables together with their values"

# Текст при вводе значения для переменной для рандомайзера
WRITE_VALUE_FOR_VARIABLE_FOR_RANDOMIZER_TEXT = '✅ You have successfully entered the value "{}" for the variable "{}"! \nNow you can add another value for this variable or press the button below to finish entering values:'

# Текст при выборе переменной для рандомайзера
SELECT_VARIABLE_FOR_RANDOMIZER_TEXT = '✅ You have successfully selected the variable "{}"! \nPress the buttons below for actions with it:'

# Текст при нажатии кнопки "➕ Добавить значения" для переменной в рандомайзере
ADD_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT = (
    'Enter new values for the variable "{}" to add to the current values:'
)

# Текст при нажатии кнопки "🗑️ Удалить значение" для переменной в рандомайзере
DELETE_VALUES_FOR_VARIABLE_FOR_RANDOMIZER_TEXT = (
    'Select the value you want to delete from the variable "{}":'
)

# Текст при удалении всех значений из переменной
ALL_VALUES_DELETED_TEXT = '✅ All values have been successfully deleted from the variable "{}"!'

# Текст при ошибке ввода переменной для рандомайзера
VARIABLE_ALREADY_EXISTS_TEXT = (
    "❌ Such a variable already exists! Try entering a different variable."
)

# Текст при получении промпта для рандомайзера
GET_PROMPT_FOR_RANDOMIZER_SUCCESS_TEXT = "✅ Prompt for the randomizer received successfully! \nCurrent randomizer prompt: \n<code>{}</code>"

# Текст при отсутствии промпта для рандомайзера
PROMPT_FOR_RANDOMIZER_NOT_WRITTEN_TEXT = "❌ The randomizer prompt has not been entered! Please enter a prompt for the randomizer."

# Текст при отсутствии переменных для рандомайзера
VARIABLES_FOR_RANDOMIZER_NOT_WRITTEN_TEXT = "❌ Randomizer variables have not been entered! Please enter variables for the randomizer."

# Текст при отсутствии модели
MODEL_NOT_FOUND_TEXT = "❌ Model with number {} not found! Try entering a different number. All allowed numbers: {}"

# Текст при неверном вводе номера модели
WRONG_MODEL_INDEX_TEXT = (
    '❌ The model number "{}" is not a number! Try entering a different number.'
)

# Текст при получении названия модели и запроса ввести промпт
GET_MODEL_INDEX_SUCCESS_TEXT = (
    "✅ Now enter your prompt:"
)

# Текст при получении номера модели и запроса выбрать тип написания промпта
GET_MODELS_INDEXES_AND_WRITE_PROMPT_TYPE_SUCCESS_TEXT = "✅ Model numbers received successfully! Now choose the prompt writing mode:"

# Текст при получении названий моделей и запроса ввести промпт
GET_MODEL_INDEXES_SUCCESS_TEXT = (
    "✅ Model numbers received successfully! Now enter your prompt:"
)

# Текст о генерации изображений по имени модели
GENERATE_IMAGES_BY_MODEL_NAME_TEXT = (
    "Generating images for model {} with number {}..."
)

# Текст для присылания изображения для генерации видео
SEND_IMAGES_FOR_VIDEO_GENERATION = (
    '👇 Send all the required images (as photos, not files) for video generation, and after that press the button below "✅ Done":'
)

# Текст при отсутствии изображения для генерации видео
NO_IMAGE_FOR_VIDEO_GENERATION_ERROR_TEXT = "❌ Could not detect an image in the message! Please send the image for video generation again."

# Текст для ввода промпта на генерацию видео из фото
WRITE_PROMPT_FOR_VIDEO_GENERATION_FROM_IMAGE_TEXT = (
    "✒️ Write your prompt by which a video will be generated:"
)

# Текст для ввода промпта на генерацию нескольких видео из фото
WRITE_PROMPT_FOR_MULTI_VIDEO_GENERATION_FROM_IMAGE_TEXT = (
    "✒️ Write your prompt by which the videos will be generated ({}):"
)

# Текст для ввода имени модели для сохранения видео
SUCCESS_VIDEO_GENERATION_FROM_IMAGE_TEXT = "✅ The video has been generated successfully! Choose an action for the generated video:"

# Текст при недостаточном балансе
KLING_INSUFFICIENT_BALANCE_TEXT = "Insufficient funds on Kling!"

# Текст для того, чтобы пользователь написал имя модели
WRITE_MODELS_NAME_TEXT = """
✅ Enter the model number (for multiple generation — model numbers separated by a comma) for generation:
"""

WRITE_MULTI_PROMPTS_FOR_SPECIFIC_GENERATION = """
✅
You need to enter the model number and prompt in the following format:
Model number - prompt
Model number - prompt

Example:
1 - prompt
2 - prompt

When you finish entering prompts in this message (or the messages below) press the "✅ Done" button.
‼️ You need to press this button only once under one of the messages. Repeated pressing may cause errors.
"""

# Текст для ввода уникальных промптов в img2video
WRITE_MULTI_PROMPTS_FOR_IMG2VIDEO = """
✅
You need to enter a prompt and model for each image in the following format:
Image number - prompt - model number
Image number - prompt - model number

Example:
1 - a beautiful girl on the beach - 1
2 - an elegant woman in the city - 2

When you finish entering prompts in this message (or the messages below) press the "✅ Done" button.
‼️ You need to press this button only once under one of the messages. Repeated pressing may cause errors.
"""

# Текст при перегенерировании изображения с новым промптом
WRITE_NEW_PROMPT_TEXT = (
    "✅ Enter a new prompt to regenerate the image:"
)

# Текст при ошибке генерации изображений по имени модели
GENERATE_IMAGE_ERROR_TEXT = "An error occurred while generating images for model {} with number {}! \nError text: <code>{}</code>"

# Текст для ввода имени модели для сохранения видео
ASK_FOR_MODEL_NAME_FOR_VIDEO_GENERATION_FROM_IMAGE_TEXT = (
    "✒️ Enter the model ordinal number whose folder the video will be saved to:"
)

# Текст для ожидания пока сгенерируется первое видео
WAIT_FOR_VIDEO_GENERATION_TEXT = "🔄 Waiting for the first video to be generated..."

# Текст при перегенерации видео
REGENERATE_VIDEO_TEXT = (
    "🔄 Regenerating the video for model {} with number {}..."
)

# Ошибки при замене лица
FACE_SWAP_TIMEOUT_ERROR_TEXT = (
    "❌ Face swap timeout (30 minutes) for model {} (#{}) was exceeded."
)

# Текст при выборе режима одного сообщения для рандомайзера
ONE_MESSAGE_FOR_RANDOMIZER_TEXT = """
✅ You have successfully selected the single-message mode for the randomizer!
It is used to enter all variables and values using a single message.
Input format:
<code>
Variable 1: value 1/value 2/value 3;
Variable 2: value 1/value 2/value 3;
Variable 3: value 1/value 2/value 3;
</code>
Example:
<code>
location: sea/forest/city;
clothing: jeans/t-shirt/dress;
time: morning/afternoon/evening;
</code>

When you finish entering all variables and values, press the "✅ Done" button on this message
"""

# Сообщение об успешном вводе одного сообщения для рандомайзера
ONE_MESSAGE_FOR_RANDOMIZER_SUCCESS_TEXT = "✅ Variable processing finished"

# Текст при ошибке ввода одного сообщения для рандомайзера
ONE_MESSAGE_FOR_RANDOMIZER_ERROR_TEXT = "An error occurred while processing the message. Please check the format and try again."

# Текст при отсутствии изображения
IMAGE_NOT_FOUND_TEXT = "❌ Image for upscale and face swap not found!"

# Текст при отмене предыдущих работ
CANCEL_PREVIOUS_JOBS_TEXT = "🔄 Canceling previous jobs..."

# Текст при пустом промпте
EMPTY_PROMPT_TEXT = (
    "❌ The prompt cannot be empty! Please enter a prompt."
)

# Текст при неверном вводе номера модели
NOT_NUMBER_TEXT = (
    "❌ The entered value is not a number! Please enter a number."
)

# Текст при неверной форме сообщения
WRONG_FORMAT_TEXT = (
    "❌ The entered message does not match the format! Please enter the message in the correct format."
)

# Текст при дублировании чисел в номерах моделей
DUPLICATE_NUMBERS_TEXT = (
    "❌ The entered model numbers are duplicated! Please enter model numbers without duplication."
)

# Текст при успешном получении изображения для генерации видео
SUCCESS_GET_IMAGE_FOR_VIDEO_GENERATION_TEXT = "✅ Image processing completed successfully!"

# Текст при успешном получении изображений для генерации видео
SUCCESS_GET_IMAGES_FOR_VIDEO_GENERATION_TEXT = "✅ Processing of {} images completed successfully!"

# Текст при просьбе для пользователя отправить имена моделей для всех отправленных изображений
GET_MODEL_INDEXES_FOR_ALL_IMAGES_TEXT = """
✅ Enter the model indexes for all sent images ({}) in the format:
Image number - model number

Example:
1 - 1
2 - 2
3 - 3
"""

# Текст при неверном формате при вводе индексов моделей для всех отправленных изображений
WRONG_FORMAT_FOR_MODEL_INDEXES_FOR_ALL_IMAGES_TEXT = "❌ The entered message does not match the format! Please enter the message in the correct format. The error was in the line: {}"

# Текст при отсутствии изображений для генерации видео
NO_IMAGES_FOR_VIDEO_GENERATION_ERROR_TEXT = "❌ There are no images for video generation! Please send the images for video generation again."

# Текст при неверном количестве индексов моделей для всех отправленных изображений
WRONG_AMOUNT_OF_MODEL_INDEXES_FOR_ALL_IMAGES_TEXT = "❌ The number of entered model indexes does not match the number of images! Please enter the model indexes for all sent images again."

# Текст при успешной обработке в режиме нескольких сообщений
MESSAGE_IS_SUCCESFULLY_DONE = "✅ The message has been processed successfully!"

# Текст при ошибке при перегенерации изображения
REGENERATE_IMAGE_ERROR_TEXT = "❌ An error occurred while regenerating the image for model {} with number {}! \nError text: <code>{}</code>"

# Текст при начале уменьшения разрешения изображения
RESIZE_IMAGE_TEXT = "🔄 Reducing the image resolution using ILoveAPI... (1/2)"

# Текст при начале Upscale с помощью Magnific Upscaler
MAGNIFIC_UPSCALE_TEXT = "🪄 Upscaling the image using Magnific Upscaler... (2/2)"

# Текст со статистикой о каждой ошибке
ERRORS_STATS_TEXT = """
⚙️ Summary of failed actions in the current generation:

Fooocus Upscale errors:
{}

Second Upscale errors:
{}

Face swap errors:
{}

Image saving errors:
{}

Video generation errors:
{}
"""

# Текст когда все изображения успешно сохранены
ALL_IMAGES_SUCCESSFULLY_SAVED_TEXT = "✅ All images have been saved successfully!"

# Текст для ввода промпта на генерацию видео по 1 промпту
WRITE_PROMPT_FOR_VIDEO_GENERATION_BY_ONE_PROMPT_TEXT = "✒️ Write your prompt by which videos will be generated for all saved images in the current generation:"

# Текст для спрашивания произвести ли повторную генерацию
ASK_FOR_NEW_GENERATION_TEXT = "Generation completed successfully! ✅\n✒️ Start a new generation?"