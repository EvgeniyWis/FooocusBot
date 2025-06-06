import asyncio

import httpx
from aiogram import types
from aiogram.fsm.context import FSMContext
from config import RUNPOD_HEADERS, RUNPOD_HOST
from logger import logger
from .. import text
from .getEndpointID import getEndpointID


# Функция для получения статуса работы
async def checkJobStatus(
    job_id: str,
    setting_number: int,
    state: FSMContext = None,
    message: types.Message = None,
    is_test_generation: bool = False,
    checkOtherJobs: bool = True,
    timeout: int = 600 * 100,
):
    start_time = asyncio.get_event_loop().time()

    while True:
        if asyncio.get_event_loop().time() - start_time > timeout:
            raise TimeoutError(
                "Превышено время ожидания статуса работы",
            )

        try:
            # Получаем ID эндпоинта для генерации изображений
            ENDPOINT_ID = await getEndpointID(setting_number)

            # Формируем URL для отправки запроса
            url = f"{RUNPOD_HOST}/{ENDPOINT_ID}/status/{job_id}"
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.post(
                    url,
                    headers=RUNPOD_HEADERS,
                )
                response_json = response.json()

            logger.info(
                f"Получен статус работы c id {job_id}: {response_json['status']}",
            )
        except Exception as e:
            logger.error(
                f"Ошибка при получении статуса работы: {e} \nОтвет: {response.text}",
            )
            await asyncio.sleep(10)
            continue

        if state and message and not is_test_generation and checkOtherJobs:
            stateData = await state.get_data()

            if "jobs" in stateData:
                jobs = stateData["jobs"]
                total_jobs_count = stateData["total_jobs_count"]
                jobs[job_id] = response_json["status"]
                await state.update_data(jobs=jobs)

                # Получаем стейт и изменяем сообщение
                success_images_count = len(
                    [job for job in jobs.values() if job == "COMPLETED"],
                )
                error_images_count = len(
                    [job for job in jobs.values() if job == "FAILED"],
                )
                progress_images_count = len(
                    [job for job in jobs.values() if job == "IN_PROGRESS"],
                )
                queue_images_count = len(
                    [job for job in jobs.values() if job == "IN_QUEUE"],
                )
                cancelled_images_count = len(
                    [job for job in jobs.values() if job == "CANCELLED"],
                )
                left_images_count = total_jobs_count - len(jobs)
                total_images_count = (
                    success_images_count
                    + error_images_count
                    + progress_images_count
                    + queue_images_count
                    + left_images_count
                    + cancelled_images_count
                )

                # Добавляем в стейт то, сколько готовых изображений
                await state.update_data(total_images_count=total_images_count)

                try:
                    await message.edit_text(
                        text.GENERATE_IMAGES_PROCESS_TEXT.format(
                            success_images_count,
                            error_images_count,
                            cancelled_images_count,
                            progress_images_count,
                            queue_images_count,
                            left_images_count,
                        ),
                    )
                except:
                    pass
            else:
                # Добавляем в стейт то, сколько готовых изображений
                await state.update_data(total_images_count=1)

        if response_json["status"] == "COMPLETED":
            break

        elif response_json["status"] in ["FAILED", "CANCELLED"]:
            if response_json["status"] == "FAILED":
                raise Exception(response_json["error"])
            
            response_json = None

            break

        await asyncio.sleep(10)

    # Когда работа завершена, получаем изображение
    logger.info(f"Работа по id {job_id} завершена!")

    # Удаляем id работы из стейта
    if state:
        stateData = await state.get_data()
        image_generation_jobs = stateData.get("image_generation_jobs", [])
        
        # Находим и удаляем задачу по job_id
        image_generation_jobs = [job for job in image_generation_jobs if job['job_id'] != job_id]
        await state.update_data(image_generation_jobs=image_generation_jobs)
        logger.info(f"Удаляем id работы {job_id} из стейта {image_generation_jobs}")
    
    return response_json
