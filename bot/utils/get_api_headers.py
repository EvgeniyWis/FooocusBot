from typing import Any

from bot.settings import settings


def get_runpod_headers() -> dict[str, Any]:
    api_key = settings.RUNPOD_API_KEY
    return {
        "Content-Type": "application/json",
        "Authorization": api_key,
    }


def get_kling_headers() -> dict[str, Any]:
    api_key = settings.KLING_API_KEY
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
