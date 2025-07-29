from enum import Enum


class PodStatus(Enum):
    RUNNING = "running"
    ALREADY_RUNNING = "already_running"
    NOT_FOUND = "not_found"
    NOT_ENOUGH_FREE_GPU = "not_enough_free_gpu"
    ERROR = "error"
    TIMEOUT = "timeout"
    START_REQUESTED = "start_requested"
