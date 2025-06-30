import json
import os

import aiofiles


class ComfyUIMetricsService:
    def __init__(self, path: str, avg_count: int = 10):
        self.path = path
        self.avg_count = avg_count

    async def save(self, duration: float):
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

    async def get_avg(self) -> float:
        if not os.path.exists(self.path):
            return 3600.0
        async with aiofiles.open(self.path, "r") as f:
            content = await f.read()
            times = json.loads(content) if content else []
        return sum(times) / len(times) if times else 3600.0
