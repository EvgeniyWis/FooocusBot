from typing import Optional, TypedDict


class TaskFileFormat(TypedDict):
    server_filename: str
    filename: str
    rotate: Optional[int]
    password: Optional[str]
