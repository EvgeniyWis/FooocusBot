import json
import os

import aiofiles

from bot.logger import logger


class ComfyUIMetricsService:
    def __init__(self, path: str, avg_count: int = 10):
        self.path = path
        self.avg_count = avg_count
        logger.debug(
            f"Инициализирован сервис метрик. Путь: {path}, усреднение по {avg_count} записям",
        )

    async def save(self, duration: float):
        logger.debug(f"Сохранение нового времени генерации: {duration:.2f}с")
        try:
            if os.path.exists(self.path):
                async with aiofiles.open(self.path, "r") as f:
                    content = await f.read()
                    times = json.loads(content) if content else []
            else:
                times = []

            times.append(duration)
            times = times[-self.avg_count :]

            async with aiofiles.open(self.path, "w") as f:
                await f.write(json.dumps(times))
            logger.info(
                f"Время генерации успешно сохранено. Текущий размер истории: {len(times)}",
            )
        except Exception as e:
            logger.error(f"Ошибка при сохранении времени генерации: {str(e)}")
            raise

    async def get_avg(self) -> float:
        try:
            if not os.path.exists(self.path):
                logger.info(
                    "Файл метрик не найден, возвращаем значение по умолчанию - 1 час",
                )
                return 3600.0

            async with aiofiles.open(self.path, "r") as f:
                content = await f.read()
                times = json.loads(content) if content else []

            if not times:
                logger.info(
                    "Нет записей о времени генерации, возвращаем значение по умолчанию",
                )
                return 3600.0

            avg = sum(times) / len(times)
            logger.debug(
                f"Рассчитано среднее время генерации: {avg:.2f}с на основе {len(times)} записей",
            )
            return avg
        except Exception as e:
            logger.error(
                f"Ошибка при расчете среднего времени генерации: {str(e)}",
            )
            return 3600.0  # Возвращаем значение по умолчанию при ошибке


# todo: не работают метрики
