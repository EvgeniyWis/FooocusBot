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
    stdout, stderr = await process.communicate()
    stdout_str = stdout.decode()
    stderr_str = stderr.decode()
    if process.returncode != 0 or not os.path.exists(output_path):
        if (
            "Processing to image failed" in stderr_str
            or "Finalizing image skipped" in stderr_str
        ):
            raise ValueError(
                "FaceFusion не смог заменить лицо на изображении (возможно, не распознано лицо)",
            )

        raise RuntimeError(
            f"FaceFusion завершился с ошибкой (code={process.returncode}) и файл не создан:\n"
            f"STDOUT:\n{stdout_str}\n\nSTDERR:\n{stderr_str}",
        )

    logger.info(
        f"FaceFusion успешно завершен, результат: {output_path}, status_code: {process.returncode}",
    )
    logger.info(
        f"Содержимое папки results перед чтением: {os.listdir(constants.FACEFUSION_RESULTS_DIR)}",
    )
    logger.info(f"Файл сохранен?: {os.path.exists(output_path)}")

    return str(output_path)
