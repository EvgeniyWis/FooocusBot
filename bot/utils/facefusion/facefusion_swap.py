import asyncio
import os
import uuid

import aiofiles

import bot.constants as constants
from bot.logger import logger
from bot.settings import settings


async def facefusion_swap(source_filename: str, target_filename: str) -> str:
    """
    Выполняет подмену лица через FaceFusion внутри Docker-контейнера.

    :param source_filename: путь к исходному изображению относительно папки .assets/ (с которого взять лицо)
    :param target_filename: путь к целевому изображению относительно папки .assets/  (куда вставить лицо)
    :return: абсолютный путь к выходному изображению
    """
    output_filename = f"{uuid.uuid4()}_output.jpg"
    output_path = os.path.join(
        constants.FACEFUSION_RESULTS_DIR,
        output_filename,
    )

    FACEFUSION_CONTAINER_NAME = os.getenv("FACEFUSION_CONTAINER_NAME")

    logger.info(f"FACEFUSION_CONTAINER_NAME: {FACEFUSION_CONTAINER_NAME}")

    docker_cmd = [
        "docker",
        "exec",
        settings.FACEFUSION_CONTAINER_NAME,
        "python",
        "facefusion.py",
        "headless-run",
        "--source",
        f"{source_filename}",
        "--target",
        f"{target_filename}",
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
        else:
            stderr_decoded = stderr.decode().strip()
            if stderr_decoded:
                stderr_lines = stderr_decoded.splitlines()

                # Пропускаем все строки с affinity warning'ами
                filtered_lines = [
                    line
                    for line in stderr_lines
                    if "pthread_setaffinity_np failed" not in line
                ]

                if filtered_lines:
                    logger.warning(
                        "FaceFusion stderr (non-affinity):\n"
                        + "\n".join(filtered_lines),
                    )
                else:
                    logger.debug(
                        "Все сообщения stderr — это ожидаемые ворнинги onnxruntime, игнорируем",
                    )

        async with aiofiles.open(output_path, mode="rb") as f:
            if not f.readable():
                logger.error(f"Файл {output_filename} не найден")
                raise FileNotFoundError(
                    f"Файл {output_filename} не найден. Скорее всего проблема произошла с путями",
                )

        logger.info(f"FaceFusion успешно завершен, результат: {output_path}")
        return str(output_path)

    except Exception as e:
        raise RuntimeError(f"Ошибка FaceFusion: {str(e)}")
