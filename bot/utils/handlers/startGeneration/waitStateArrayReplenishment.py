import asyncio
import time

from aiogram.fsm.context import FSMContext
from logger import logger


# Функция для ожидания пополнения массива в стейте
async def waitStateArrayReplenishment(state: FSMContext, array_name: str,
    stateNamesForCycleExit: tuple[str, str]) -> list[dict] | bool:

    try:
        start_time = time.time()  # Запоминаем время начала
        while True:
            # Проверяем, не прошло ли 2 минуты
            if time.time() - start_time > 120:  # 120 секунд = 2 минуты
                logger.warning("Превышено время ожидания (2 минуты)")
                return False

            stateData = await state.get_data()

            if not stateData[array_name]:
                array = []
            else:
                array = stateData[array_name]

            logger.info(f"Модели для генерации {array}: {[list(i.keys())[0] for i in array]}")

            if len(array) > 0:
                return array

            if stateData[stateNamesForCycleExit[0]] == stateData[stateNamesForCycleExit[1]]:
                return False

            await asyncio.sleep(5)
    except Exception as e:
        logger.error(f"Ошибка в функции waitStateArrayReplenishment: {e}")
        return False
