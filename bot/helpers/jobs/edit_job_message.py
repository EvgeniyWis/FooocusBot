from aiogram.fsm.context import FSMContext

from bot.InstanceBot import bot
from bot.helpers import text
from bot.helpers.jobs.rate_limiter_for_edit_job_message import safe_bot_edit_job_message


async def edit_job_message(
    job_id: str,
    message_id: int,
    state: FSMContext,
    response_json: dict,
    user_id: int,
) -> None:
    """
    Редактирование сообщения о процессе и статистике генерации изображений

    Args:
        job_id (str): ID работы
        message_id (int): ID сообщения, которое нужно отредактировать
        state (FSMContext): Контекст состояния
        response_json (dict): JSON ответ от API
        user_id (int): ID пользователя
    """

    state_data = await state.get_data()

    if "jobs" in state_data:
        jobs = state_data.get("jobs", {})
        total_jobs_count = state_data.get("total_jobs_count", 0)
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
            await safe_bot_edit_job_message(
                bot,
                chat_id=user_id,
                message_id=message_id,
                safe_text=text.GENERATE_IMAGES_PROCESS_TEXT.format(
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
