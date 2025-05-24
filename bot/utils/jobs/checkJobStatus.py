from utils import text
import requests
from logger import logger
from config import RUNPOD_HEADERS, RUNPOD_HOST
import asyncio
from aiogram.fsm.context import FSMContext
from aiogram import types

# Функция для получения статуса работы
async def checkJobStatus(job_id: str, state: FSMContext = None, message: types.Message = None, 
    is_test_generation: bool = False, checkOtherJobs: bool = True):
    while True:
        if state:
            data = await state.get_data()
            if "stop_generation" in data:
                if data["stop_generation"]:
                    raise Exception("Генерация остановлена")
        
        try:
            response = requests.post(f'{RUNPOD_HOST}/status/{job_id}', headers=RUNPOD_HEADERS)
            response_json = response.json()
            
            logger.info(f"Получен статус работы c id {job_id}: {response_json['status']}")
        except Exception as e:
            logger.error(f"Ошибка при получении статуса работы: {e} \nОтвет: {response_json}")
            await asyncio.sleep(10)
            continue

        if state and message and not is_test_generation and checkOtherJobs:
            stateData = await state.get_data()

            if "jobs" in stateData:
                jobs = stateData["jobs"]
                total_jobs_count = stateData["total_jobs_count"]
                jobs[job_id] = response_json['status']
                await state.update_data(jobs=jobs)
                
                # Получаем стейт и изменяем сообщение
                success_images_count = len([job for job in jobs.values() if job == 'COMPLETED'])
                error_images_count = len([job for job in jobs.values() if job == 'FAILED'])
                progress_images_count = len([job for job in jobs.values() if job == 'IN_PROGRESS'])
                queue_images_count = len([job for job in jobs.values() if job == 'IN_QUEUE'])
                left_images_count = total_jobs_count - len(jobs)

                # Добавляем в стейт то, сколько готовых изображений
                await state.update_data(success_images_count=success_images_count)

                try:
                    await message.edit_text(text.GENERATE_IMAGES_PROCESS_TEXT
                    .format(success_images_count, error_images_count, progress_images_count, queue_images_count, 
                        left_images_count))
                except Exception as e:
                    logger.error(f"Ошибка при изменении сообщения: {e}")

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

    return response_json