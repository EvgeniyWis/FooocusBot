import asyncio
import traceback

from aiogram import types
from aiogram.exceptions import TelegramRetryAfter
from aiogram.fsm.context import FSMContext

from bot.app.core.logging import logger
from bot.app.instance import bot
from bot.helpers import text
from bot.helpers.handlers.messages.deleteMessageFromState import (
    deleteMessageFromState,
)
from bot.helpers.handlers.startGeneration.process_image import process_image
from bot.utils.handlers import (
    appendDataToStateArray,
)
from bot.utils.handlers.messages import (
    safe_send_media_group,
)


# Функция для отправки сообщения со сгенерируемыми изображениями
async def sendImageBlock(
    state: FSMContext,
    media_group: list,
    model_name: str,
    group_number: str,
    user_id: int,
    job_id: str,
    model_key: str = None,
):
    try:
        # Ограничиваем media_group до 10 элементов (Telegram лимит)
        media_group = media_group[:10]
        media_group_message = await safe_send_media_group(user_id, media_group)
        if media_group_message is None:
            media_group_message = await safe_send_media_group(user_id, media_group)

        if media_group_message is None:
            logger.error(
                "media_group_message is None! Возможно, не удалось отправить медиагруппу."
            )
            raise Exception("media_group_message is None! Возможно, не удалось отправить медиагруппу.")

        if not hasattr(media_group_message, "__iter__"):
            logger.error(
                f"media_group_message не итерируемый объект: {type(media_group_message)}"
            )
            await bot.send_message(
                chat_id=user_id,
                text="Произошла ошибка при отправке изображений! (media_group_message не итерируемый)",
            )
            return
        logger.info(
            f"Media group sent to user_id={user_id}, model_name={model_name}, images_count={len(media_group)}",
        )

        await asyncio.sleep(0.7)
        logger.info(
            f"Slept 0.7s before starting auto-processing for user_id={user_id}, model_name={model_name}",
        )

        for i, message in enumerate(media_group_message):
            await appendDataToStateArray(
                state,
                "imageGeneration_mediagroup_messages_ids",
                {
                    "model_name": model_name,
                    "image_index": i,
                    "job_id": job_id,
                    "message_id": message.message_id,
                    "type": "media",
                },
                unique_keys=("model_name", "image_index", "job_id"),
            )

    except Exception as e:
        traceback.print_exc()
        logger.error(f"Ошибка при отправке медиагруппы: {e}")
        try:
            if isinstance(e, TelegramRetryAfter):
                await bot.send_message(
                    chat_id=user_id,
                    text=f"Превышен лимит отправки сообщений. Пожалуйста, подождите {e.retry_after} секунд и попробуйте снова.",
                )
            else:
                await bot.send_message(
                    chat_id=user_id,
                    text=f"Произошла ошибка при отправке изображений! Текст ошибки: {e}",
                )
        except:
            pass

    try:
        # Получаем данные из стейта
        state_data = await state.get_data()

        # Если номер группы все, то получаем номер группы из стейта
        if group_number == "all":
            group_number = state_data.get(
                "current_group_number_for_unique_prompt",
                1,
            )

        # Автоматическая обработка: запускаем процесс обработки без клавиатуры выбора
        try:
            images_count = min(len(media_group_message), 4)

            # Сообщаем пользователю, что начинается обработка всех изображений
            header_message = await bot.send_message(
                chat_id=user_id,
                text=text.SELECT_IMAGE_PROGRESS_TEXT,
            )

            # Удаляем медиагруппу изображений (и потенциальные клавиатуры, если были)
            await deleteMessageFromState(
                state,
                "imageGeneration_mediagroup_messages_ids",
                model_name,
                header_message.chat.id,
                delete_keyboard_message=True,
                job_id=job_id,
            )

            # Запускаем последовательную обработку для каждого изображения
            for image_index in range(1, images_count + 1):
                status_message = await bot.send_message(
                    chat_id=user_id,
                    text=f"🔄 Работаю с изображением для модели {model_name} под номером {image_index}... ({image_index}/{images_count})",
                )

                fake_call = types.CallbackQuery(
                    id=f"{job_id[:8]}_{image_index}",
                    from_user=types.User(id=user_id, is_bot=False, first_name="User"),
                    chat_instance="",
                    message=status_message,
                    data=f"auto_process|{model_name}|{group_number}|{image_index}|{job_id[:8]}",
                )

                logger.info(
                    f"Запускаем автоматическую обработку изображения {image_index}/{images_count} для модели {model_name} (job_id={job_id})",
                )

                try:
                    await process_image(
                        fake_call,
                        state,
                        model_name,
                        image_index,
                        model_key=model_key,
                    )
                except Exception as e:
                    logger.error(
                        f"Ошибка при обработке изображения {image_index}: {e}",
                    )
                    try:
                        await bot.send_message(
                            chat_id=user_id,
                            text=f"❌ Ошибка при обработке изображения {image_index}: {str(e)}",
                        )
                    except Exception:
                        pass
        except Exception as e:
            logger.error(f"Ошибка при автозапуске обработки изображения: {e}")
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text="❌ Произошла ошибка при запуске обработки изображения",
                )
            except Exception:
                pass
    except Exception as e:
        raise Exception(f"Произошла ошибка в функции sendImageBlock: {e}")
