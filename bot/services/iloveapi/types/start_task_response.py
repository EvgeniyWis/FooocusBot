from typing import TypedDict


class StartTaskResponse(TypedDict):
    server: str
    task: str
    remaining_credits: int 
