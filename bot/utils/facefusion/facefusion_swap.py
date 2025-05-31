import asyncio
import uuid

import aiofiles
from config import FACEFUSION_RESULTS_DIR
from logger import logger
import os

# Настройка логирования


CONTAINER_NAME = "facefusion-docker-facefusion-cpu-1"


async def facefusion_swap(source_filename: str, target_filename: str) -> str:
    """
    Выполняет подмену лица через FaceFusion внутри Docker-контейнера.

    :param source_filename: путь к исходному изображению относительно папки .assets/ (с которого взять лицо)
    :param target_filename: путь к целевому изображению относительно папки .assets/  (куда вставить лицо)
    :return: абсолютный путь к выходному изображению
    """
    output_filename = f"{uuid.uuid4()}_output.jpg"
    output_path = os.path.join(FACEFUSION_RESULTS_DIR, output_filename)


    docker_cmd = [
        "docker",
        "exec",
        CONTAINER_NAME,
        "python",
        "facefusion.py",
        "headless-run",
        "--source",
        f"/facefusion/.assets/{source_filename}",
        "--target",
        f"/facefusion/.assets/{target_filename}",
        "--output-path",
        f"/facefusion/.assets/images/results/{output_filename}",
    ]

    try:
        logger.info(
            f"Запуск FaceFusion для source: {source_filename}, target: {target_filename}",
        )
        process = await asyncio.create_subprocess_exec(
            *docker_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            logger.error(
                f"FaceFusion завершился с ошибкой: {stderr.decode().strip()}",
            )
            raise RuntimeError(f"FaceFusion failed: {stderr.decode().strip()}")

        async with aiofiles.open(output_path, mode="rb") as f:
            if not await f.readable():
                logger.error(f"Файл {output_filename} не найден")
                raise FileNotFoundError(
                    f"Файл {output_filename} не найден. Скорее всего проблема произошла с путями",
                )

        logger.info(f"FaceFusion успешно завершен, результат: {output_path}")
        return str(output_path)

    except Exception as e:
        raise RuntimeError(f"Ошибка FaceFusion: {str(e)}")
