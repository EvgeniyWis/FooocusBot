import asyncio
import http.client
import socket
import traceback

import httpx

from bot.logger import logger


# Функция для повторной операции
async def retryOperation(operation, max_attempts, delay, *args):
    """
    Выполняет операцию с повторными попытками при ошибках.
    
    Args:
        operation: Асинхронная функция для выполнения
        max_attempts: Максимальное количество попыток
        delay: Начальная задержка между попытками в секундах
        *args: Аргументы для передачи в операцию
    """
    for attempt in range(max_attempts):
        try:
            logger.info(f"Попытка {attempt + 1} из {max_attempts}")
            return await operation(*args)
            
        except (FileNotFoundError, ValueError, TypeError, RuntimeError, socket.gaierror, 
                http.client.RemoteDisconnected, http.client.HTTPException, ConnectionError, 
                OSError, httpx.ReadTimeout, httpx.ConnectTimeout, httpx.TimeoutException,
                httpx.RemoteProtocolError, httpx.ConnectError) as e:
            
            traceback.print_exc()
            
            if attempt == max_attempts - 1:
                logger.error(f"Все {max_attempts} попыток исчерпаны. Последняя ошибка: {str(e)}")
                raise e
                
            # Экспоненциальная задержка с максимальным ограничением
            current_delay = min(delay * (2 ** attempt), 300)  # максимум 5 минут
            
            logger.warning(
                f"Попытка {attempt + 1} не удалась: {str(e)}. "
                f"Повторная попытка через {current_delay:.1f} сек. "
                f"(попытка {attempt + 1}/{max_attempts})"
            )
            
            await asyncio.sleep(current_delay)
