from aiogram.fsm.context import FSMContext
from logger import logger
import asyncio


# Функция для ожидания пополнения массива в стейте
async def waitStateArrayReplenishment(state: FSMContext, array_name: str, 
    stateNamesForCycleExit: tuple[str, str]) -> list[dict] | bool:

    try:
        while True:
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
