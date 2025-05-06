import requests
import os
import asyncio
from logger import logger
from aiogram import types
from utils import text
from utils.generateImages.base64_to_image import base64_to_image
from aiogram.fsm.context import FSMContext


# Функция для генерации изображений с помощью API
async def generateImage(message: types.Message, data: dict, state: FSMContext, folder_name: str, index: int):
    # Делаем запрос на генерацию
    headers = {
        "Content-Type": "application/json",
        'Authorization': os.getenv("RUNPOD_API_KEY")
    }

    host = "https://api.runpod.ai/v2/6aqbs4lkswywz2"

    logger.info(f"Отправка запроса на генерацию...")

    # Получаем id работы
    response = requests.post(f'{host}/run', headers=headers, json=data)
    response_json = response.json()
    
    job_id = response_json['id']

    logger.info(f"Получен id работы: {job_id}")

    # Проверяем статус работы, пока она не будет завершена
    data = await state.get_data()
    jobs = data["jobs"]

    while True:
        response = requests.post(f'{host}/status/{job_id}', headers=headers)
        response_json = response.json()

        logger.info(f"Получен статус работы c id {job_id}: {response_json['status']}")

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
        image_data = response_json["output"][0]["base64"]
    except Exception as e:
        raise Exception(f"Ошибка при получении изображения: {e}")
    
    return await base64_to_image(image_data, folder_name, index)

