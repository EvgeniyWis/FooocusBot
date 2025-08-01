import asyncio
import traceback

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.helpers import text
from bot.helpers.generateImages.dataArray import getDataByModelName
from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)
from bot.helpers.generateImages.dataArray.getDataArrayByRandomizer import (
    getDataArrayByRandomizer,
)
from bot.utils.handlers.messages.rate_limiter_for_send_message import (
    safe_send_message,
)


# Функция для генерации изображений по всем группам
async def generate_images_by_all_groups(
    message: types.Message,
    state: FSMContext,
    user_id: int,
    is_test_generation: bool,
    variable_prompt: str,
    with_randomizer: bool = False,
):
    """
    Генерирует изображения по всем группам

    Args:
        message: types.Message - сообщение с прогрессом генерации
        state: FSMContext - контекст состояния
        user_id: int - id пользователя
        is_test_generation: bool - флаг тестовой генерации
        variable_prompt: str - переменный промпт
        with_randomizer: bool - флаг использования рандомайзера

    Returns:
        bool - флаг успешности генерации
    """
    from bot.helpers.generateImages.generateImageBlock import (
        generateImageBlock,
    )

    # Получаем все группы
    dataArrays = getAllDataArrays()
    groups_numbers_success = []
    semaphore = asyncio.Semaphore(5)

    # Добавляем рандомные значения к промпу
    if with_randomizer:
        dataArrays = [
            await getDataArrayByRandomizer(state, i + 1 if i + 1 != len(dataArrays) else "extra")
            for i in range(len(dataArrays))
        ]

    # Создаём сообщение с прогрессом генерации настроек
    message_with_groups = await safe_send_message(
        text=text.TEST_GENERATION_WITH_ALL_GROUPS_PROGRESS_TEXT.format(
            "❌",
            "❌",
            "❌",
            "❌",
        ),
        message=message,
    )

    await message_with_groups.pin()

    # Создаём сообщение с прогрессом генерации изображений
    message_with_generations_status = await safe_send_message(
        text=text.GET_PROMPT_SUCCESS_TEXT,
        message=message,
    )

    if not is_test_generation:
        await message_with_generations_status.pin()

    async def process_generation(model_name, index, prompt):
        async with semaphore:
            # Получаем данные генерации по названию модели
            data = await getDataByModelName(model_name)

            await generateImageBlock(
                data,
                message_with_generations_status.message_id,
                state,
                user_id,
                model_name,
                prompt,
                is_test_generation,
                chat_id=message.chat.id,
            )

    try:
        for index, dataArray in enumerate(dataArrays):
            tasks = []
            if is_test_generation:
                model_name = dataArray[0]["model_name"]
                task = asyncio.create_task(
                    process_generation(model_name, index, variable_prompt),
                )
                tasks.append(task)
            else:
                for data in dataArray:
                    # Получаем данные
                    model_name = data["model_name"]

                    # Обновляем стейт
                    jobs = {}
                    await state.update_data(jobs=jobs)
                    await state.update_data(total_jobs_count=len(dataArray))

                    # Генерируем изображение
                    task = asyncio.create_task(
                        process_generation(model_name, index, variable_prompt),
                    )
                    tasks.append(task)

            await asyncio.gather(*tasks)
            groups_numbers_success.append(index)

            await message_with_groups.edit_text(
                text.TEST_GENERATION_WITH_ALL_GROUPS_PROGRESS_TEXT.format(
                    "✅" if 0 in groups_numbers_success else "❌",
                    "✅" if 1 in groups_numbers_success else "❌",
                    "✅" if 2 in groups_numbers_success else "❌",
                    "✅" if 3 in groups_numbers_success else "❌",
                ),
            )

        await message_with_groups.unpin()
        await message_with_generations_status.unpin()
        return True
    except Exception as e:
        await message_with_groups.unpin()
        await message_with_generations_status.unpin()
        traceback.print_exc()
        raise Exception(
            f"Произошла ошибка при генерации изображений по всем группам: {e}",
        )
