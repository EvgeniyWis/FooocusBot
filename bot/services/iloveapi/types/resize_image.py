from typing import TypedDict


class ToolDataResizeImage(TypedDict):
    pixels_width: int
    pixels_height: int
    maintain_ratio: bool
