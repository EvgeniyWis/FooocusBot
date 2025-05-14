import asyncio
import uuid
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent.parent.parent.parent.absolute()
ASSETS_DIR = SCRIPT_DIR / "facefusion-docker" / ".assets" / "images" / "results"
CONTAINER_NAME = "facefusion-docker-facefusion-cpu-1"


async def facefusion_swap(source_filename: str, target_filename: str) -> str:
    """
    Выполняет подмену лица через FaceFusion внутри Docker-контейнера.

    :param source_filename: путь к исходному изображению относительно папки .assets/ (с которого взять лицо)
    :param target_filename: путь к целевому изображению относительно папки .assets/  (куда вставить лицо)
    :return: абсолютный путь к выходному изображению
    """
    output_filename = f"{uuid.uuid4()}_output.jpg"
    output_path = ASSETS_DIR / output_filename

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
        process = await asyncio.create_subprocess_exec(
            *docker_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        await asyncio.sleep(1)

        if process.returncode != 0:
            raise RuntimeError(f"FaceFusion failed: {stderr.decode().strip()}")

        if not output_path.exists():
            raise FileNotFoundError(
                f"Файл {output_filename} не найден. Скорее всего проблема произошла с путями",
            )

        return str(output_path)

    except Exception as e:
        raise RuntimeError(f"Ошибка FaceFusion: {str(e)}")