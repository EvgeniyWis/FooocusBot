import asyncio
import os
import uuid

import bot.constants as constants
from bot.logger import logger
from bot.settings import settings


async def facefusion_swap(source_filename: str, target_filename: str) -> str:
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

    logger.info(
        f"Запуск FaceFusion для source: {source_filename}, target: {target_filename}",
    )
    process = await asyncio.create_subprocess_exec(
        *docker_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await process.communicate()

    logger.info(f"FaceFusion успешно завершен, результат: {output_path}")

    # Проверяем, что файл существует
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Facefusion не смог сделать замену лица для изображения!")

    return str(output_path)
