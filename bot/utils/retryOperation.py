import asyncio
import http.client
import socket
import traceback

from bot.logger import logger


# Функция для повторной операции
async def retryOperation(operation, max_attempts=3, delay=2, *args):
    for attempt in range(max_attempts):
        try:
            return await operation(*args)
        except (FileNotFoundError, ValueError, TypeError, RuntimeError, socket.gaierror, http.client.RemoteDisconnected, http.client.HTTPException, ConnectionError, OSError) as e:
            traceback.print_exc()
            if attempt == max_attempts - 1:
                raise e
            logger.warning(
                f"Попытка {attempt + 1} не удалась: {str(e)}. Повторная попытка через {delay} сек.",
            )
            await asyncio.sleep(delay)
            delay *= 1.2
