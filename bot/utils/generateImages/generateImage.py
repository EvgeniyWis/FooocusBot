import requests
import os
import asyncio
from config import ENDPOINT_ID, TEMP_FOLDER_PATH
from .dataArray.getAllDataArrays import getAllDataArrays
from logger import logger
from aiogram import types
from utils.text import text
from utils.generateImages.base64ToImage import base64ToImage
from aiogram.fsm.context import FSMContext
from keyboards.user import keyboards
import shutil
import traceback


# Функция для генерации изображений по объекту данных
async def generateByData(dataJSON: dict, model_name: str, message: types.Message, state: FSMContext, 
    user_id: int, setting_number: str, is_test_generation: bool = False, checkOtherJobs: bool = True):
    # Делаем запрос на генерацию
    headers = {
        "Content-Type": "application/json",
        'Authorization': os.getenv("RUNPOD_API_KEY")
    }

    host = f"https://api.runpod.ai/v2/{ENDPOINT_ID}"
    logger.info(f"Отправка запроса на генерацию: {dataJSON}")

    # Получаем id работы
    max_attempts = 5
    attempt = 0
    while True:
        attempt += 1
        try:
            response = requests.post(f'{host}/run', headers=headers, json=dataJSON)
            response_json = response.json()
            break
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Ошибка при получении статуса работы (сетевая ошибка): {e}, попытка {attempt}/{max_attempts}")
            if attempt >= max_attempts:
                raise Exception(f"Не удалось подключиться к серверу после {max_attempts} попыток")
            await asyncio.sleep(10)

    logger.info(f"Ответ на запрос: {response_json}")
    
    job_id = response_json['id']

    logger.info(f"Получен id работы: {job_id}")

    # Проверяем статус работы, пока она не будет завершена
    if checkOtherJobs:
        stateData = await state.get_data()
        jobs = stateData["jobs"]
        total_jobs_count = stateData["total_jobs_count"]

    while True:
        try:
            response = requests.post(f'{host}/status/{job_id}', headers=headers)
            response_json = response.json()
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Ошибка при получении статуса работы (сетевая ошибка): {e}")
            await asyncio.sleep(10)
            continue

        logger.info(f"Получен статус работы c id {job_id}: {response_json['status']}")

        if checkOtherJobs:
            jobs[job_id] = response_json['status']
            await state.update_data(jobs=jobs)
                
            # Получаем стейт и изменяем сообщение
            stateData = await state.get_data()
            jobs = stateData["jobs"]
            success_images_count = len([job for job in jobs.values() if job == 'COMPLETED'])
            error_images_count = len([job for job in jobs.values() if job == 'FAILED'])
            progress_images_count = len([job for job in jobs.values() if job == 'IN_PROGRESS'])
            left_images_count = len([job for job in jobs.values() if job == 'IN_QUEUE'])

        try:
            await message.edit_text(text.GENERATE_IMAGES_PROCESS_TEXT
            .format(success_images_count, error_images_count, progress_images_count, left_images_count, total_jobs_count - len(jobs)))
        except Exception as e:
            pass

        if response_json['status'] == 'COMPLETED':
            break

        elif response_json['status'] in ['FAILED', 'CANCELLED']:
            if response_json['status'] == 'FAILED':
                raise Exception(response_json['error'])
            else:
                raise Exception("Работа была отменена")

        await asyncio.sleep(10)

    # Когда работа завершена, получаем изображение
    logger.info(f"Работа по id {job_id} завершена!")

    try:
        images_output = response_json["output"]
        
        if images_output == []:
            raise Exception("Не удалось сгенерировать изображения")

        media_group = []
        base_64_dataArray = []

        # Получаем изображения и сохраняем их в массив
        for i, image_output in enumerate(images_output):
            image_data = image_output["base64"]
            base_64_data = await base64ToImage(image_data, model_name, i, user_id, is_test_generation)
            base_64_dataArray.append(base_64_data)
            media_group.append(types.InputMediaPhoto(media=types.FSInputFile(base_64_data)))
        
        # Отправляем изображения
        message_with_media_group = await message.answer_media_group(media_group)
        
        # Отправляем клавиатуру для выбора изображения
        await message.answer(text.SELECT_IMAGE_TEXT if not is_test_generation else text.SELECT_TEST_IMAGE_TEXT.format(setting_number), 
        reply_markup=keyboards.selectImageKeyboard(model_name) if not is_test_generation else None)

        # Сохраняем в стейт данные о медиагруппе, для её удаления
        await state.update_data(**{f"mediagroup_messages_ids_{model_name}": [i.message_id for i in message_with_media_group]})
        
        # Если это тестовая генерация, то удаляем изображения из папки temp/test/ и сами папки
        if is_test_generation:
            shutil.rmtree(f"{TEMP_FOLDER_PATH}/test_{user_id}")
            return
        
    except Exception as e:
        raise Exception(f"Ошибка при получении изображения: {e}")
    

# Функция для тестовой генерации по всем настройкам
async def generateTestImagesByAllSettings(message: types.Message, state: FSMContext, user_id: int,
    is_test_generation: bool, message_for_edit: types.Message = None, checkOtherJobs: bool = True):

    dataArrays = getAllDataArrays()
    settings_numbers_success = []

    try:
        for index, dataArray in enumerate(dataArrays):
            dataJSON = dataArray[0]["json"]  
            model_name = dataArray[0]["model_name"]
            picture_folder_id = dataArray[0]["picture_folder_id"]
            video_folder_id = dataArray[0]["video_folder_id"]

            await generateByData(dataJSON, model_name, message, state, user_id, index + 1, picture_folder_id, video_folder_id, is_test_generation, checkOtherJobs)

            settings_numbers_success.append(index)
            
            await message_for_edit.edit_text(text.TEST_GENERATION_WITH_ALL_SETTINGS_PROGRESS_TEXT
            .format("✅" if 0 in settings_numbers_success else "❌", 
            "✅" if 1 in settings_numbers_success else "❌", "✅" if 2 in settings_numbers_success else "❌"))

        return True
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Ошибка при тестовой генерации по всем настройкам: {e}")
        return False