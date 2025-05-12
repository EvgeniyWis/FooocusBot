import asyncio
import os
import uuid

ASSETS_DIR = "./.assets"
CONTAINER_NAME = "facefusion-cpu"


async def facefusion_swap(source_path: str, target_path: str) -> str:
    """
    Выполняет подмену лица через FaceFusion внутри Docker-контейнера.

    :param source_path: путь к исходному изображению (с которого взять лицо).
    :param target_path: путь к целевому изображению (куда вставить лицо).
    :return: путь к выходному изображению, либо исключение.
    """
    output_filename = f"{uuid.uuid4()}_output.jpg"
    output_path = os.path.join(ASSETS_DIR, output_filename)

    docker_cmd = [
        "docker",
        "exec",
        CONTAINER_NAME,
        "python",
        "facefusion.py",
        "headless-run",
        "--source",
        f"/facefusion/.assets/{os.path.basename(source_path)}",
        "--target",
        f"/facefusion/.assets/{os.path.basename(target_path)}",
        "--output-path",
        f"/facefusion/.assets/{output_filename}",
    ]

    try:
        process = await asyncio.create_subprocess_exec(
            *docker_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"FaceFusion failed: {stderr.decode().strip()}")

        if not os.path.exists(output_path):
            raise FileNotFoundError("Выходной файл не найден.")

        return output_path

    except Exception as e:
        raise RuntimeError(f"Ошибка FaceFusion: {e}")
