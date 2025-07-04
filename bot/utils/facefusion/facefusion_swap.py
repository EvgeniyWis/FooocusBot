import asyncio
import os
import uuid

import aiofiles

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

        stderr_decoded = stderr.decode().strip()
        stdout_decoded = stdout.decode().strip()

        logger.info(f"FaceFusion stdout:\n{stdout_decoded}")
        logger.info(f"FaceFusion stderr:\n{stderr_decoded}")

        if process.returncode != 0:
            stderr_decoded = stderr.decode().strip()
            stderr_lines = stderr_decoded.splitlines()
            filtered_lines = [
                line
                for line in stderr_lines
                if "pthread_setaffinity_np failed" not in line
            ]
            if filtered_lines:
                logger.error(
                    "FaceFusion завершился с ошибкой:\n"
                    + "\n".join(filtered_lines),
                )
                raise RuntimeError(
                    "FaceFusion failed:\n" + "\n".join(filtered_lines),
                )
        else:
            stderr_decoded = stderr.decode().strip()
            if stderr_decoded:
                filtered_lines = [
                    line
                    for line in stderr_decoded.splitlines()
                    if "pthread_setaffinity_np failed" not in line
                ]
                if filtered_lines:
                    logger.debug(
                        "FaceFusion stderr (non-affinity):\n"
                        + "\n".join(filtered_lines),
                    )

        if not os.path.exists(output_path):
            logger.error(f"Файл результата не найден по пути: {output_path}")
            raise FileNotFoundError(
                f"Файл результата не найден: {output_path}",
            )

        async with aiofiles.open(output_path, mode="rb") as f:
            data = await f.read()
            if not data:
                raise RuntimeError("Файл результата пустой")

        logger.info(f"FaceFusion успешно завершен, результат: {output_path}")
        return str(output_path)

    except Exception as e:
        raise RuntimeError(f"Ошибка FaceFusion: {str(e)}")
