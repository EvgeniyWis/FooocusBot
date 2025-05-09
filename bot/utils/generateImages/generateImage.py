import requests
import os
import asyncio
from logger import logger
from aiogram import types
from utils import text
from utils.generateImages.base64_to_image import base64_to_image
from aiogram.fsm.context import FSMContext
from keyboards import userKeyboards
import os
import shutil

# Функция для генерации изображений с помощью API
async def generateImage(message: types.Message, data: dict, state: FSMContext, folder_name: str, user_id: int, checkOtherJobs: bool = True):
    # Делаем запрос на генерацию
    headers = {
        "Content-Type": "application/json",
        'Authorization': os.getenv("RUNPOD_API_KEY")
    }

    host = f"https://api.runpod.ai/v2/{os.getenv('ENDPOINT_ID')}"

    logger.info(f"Отправка запроса на генерацию...")

    # Получаем id работы
    response = requests.post(f'{host}/run', headers=headers, json=data)
    response_json = response.json()
    
    job_id = response_json['id']

    logger.info(f"Получен id работы: {job_id}")

    # Проверяем статус работы, пока она не будет завершена
    if checkOtherJobs:
        data = await state.get_data()
        jobs = data["jobs"]

    while True:
        response = requests.post(f'{host}/status/{job_id}', headers=headers)
        response_json = response.json()

        logger.info(f"Получен статус работы c id {job_id}: {response_json['status']}")

        if checkOtherJobs:
            jobs[job_id] = response_json['status']
            await state.update_data(jobs=jobs)
                
            # Получаем стейт и изменяем сообщение
            data = await state.get_data()
            jobs = data["jobs"]
            success_images_count = len([job for job in jobs.values() if job == 'COMPLETED'])
            error_images_count = len([job for job in jobs.values() if job == 'FAILED'])
            progress_images_count = len([job for job in jobs.values() if job == 'IN_PROGRESS'])
            left_images_count = len([job for job in jobs.values() if job == 'IN_QUEUE'])

        try:
            await message.edit_text(text.GENERATE_IMAGES_PROCESS_TEXT
            .format(success_images_count, error_images_count, progress_images_count, left_images_count))
        except Exception as e:
            pass

        if response_json['status'] == 'COMPLETED':
            break

        elif response_json['status'] == 'FAILED':
            raise Exception(response_json['error'])

        await asyncio.sleep(10)

    # Когда работа завершена, получаем изображение
    logger.info(f"Работа по id {job_id} завершена! Ответ выглядит так: {response_json}")

    try:
        images_output = response_json["output"]
        media_group = []
        base_64_data_array = []

        # Получаем изображения и сохраняем их в массив
        for i, image_output in enumerate(images_output):
            image_data = image_output["base64"]
            base_64_data = await base64_to_image(image_data, folder_name, i, user_id, job_id)
            base_64_data_array.append(base_64_data)
            media_group.append(types.InputMediaPhoto(media=types.FSInputFile(base_64_data)))

        # Сохраняем изображения в state с индексом
        await state.update_data(**{f"images_{job_id}": base_64_data_array})
        
        # Отправляем изображения
        message_with_media_group = await message.answer_media_group(media_group)

        await state.update_data(**{f"mediagroup_messages_ids_{job_id}": [i.message_id for i in message_with_media_group]})

        # Получаем данные из state, тестовая ли это генерация
        data = await state.get_data()
        is_test_generation = data["generations_amount"] == "test"

        # Отправляем клавиатуру для выбора изображения
        await message.answer(text.SELECT_IMAGE_TEXT if not is_test_generation else text.SELECT_TEST_IMAGE_TEXT, 
        reply_markup=userKeyboards.selectImageKeyboard(job_id) if not is_test_generation else None)

        # Если это тестовая генерация, то удаляем изображения из папки temp/test/ и сами папки
        if is_test_generation:
            shutil.rmtree(f"temp/test_{user_id}")
            return
        
    except Exception as e:
        raise Exception(f"Ошибка при получении изображения: {e}")

