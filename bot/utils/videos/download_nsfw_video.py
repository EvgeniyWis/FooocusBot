import tempfile
from typing import AsyncGenerator

import aiohttp
from aiohttp import ClientError

from bot.domain.entities.video_generation import DownloadedVideo
from bot.logger import logger


async def _download_single_video(
    session: aiohttp.ClientSession,
    url: str,
    idx: int,
) -> DownloadedVideo:
    """Скачивает одно видео и возвращает результат."""
    try:
        async with session.get(url) as resp:
            if resp.status != 200:
                logger.error(
                    f"Ошибка при скачивании видео {idx}: статус {resp.status}",
                )
                return DownloadedVideo(path=None, caption=None)

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mov",
            ) as tmpfile:
                tmpfile.write(await resp.read())
                logger.info(
                    f"Видео {idx} успешно скачано, сохранено в {tmpfile.name}",
                )
                return DownloadedVideo(
                    path=tmpfile.name,
                    caption=f"Видео {idx}",
                )
    except ClientError as e:
        logger.error(f"Ошибка сети при скачивании видео {idx}: {e}")
        return DownloadedVideo(path=None, caption=None)
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при скачивании видео {idx}: {e}")
        return DownloadedVideo(path=None, caption=None)


async def download_nsfw_videos(
    video_urls: list[str],
) -> AsyncGenerator[DownloadedVideo, None]:
    """
    Асинхронно скачивает видео по списку URL.

    Args:
        video_urls: Список URL видео для скачивания

    Yields:
        DownloadedVideo с путем к скачанному файлу и подписью,
        или с None если произошла ошибка
    """
    async with aiohttp.ClientSession() as session:
        for idx, url in enumerate(video_urls, 1):
            try:
                video = await _download_single_video(session, url, idx)
                yield video
            except Exception as e:
                logger.error(f"Ошибка при обработке видео {idx}: {e}")
                yield DownloadedVideo(path=None, caption=None)
