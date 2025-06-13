from abc import ABC, abstractmethod


class ITaskStorage(ABC):
    @abstractmethod
    async def append_task(self, task: dict[str, Any]) -> None:
        """
        Append a task to the storage.
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def delete_task(self, job_id: str) -> None:
        """
        Delete a task from the storage by its job ID.
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def get_tasks(self) -> list: 
        """
        Get all tasks from the storage.
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def recover_tasks(self, callback) -> None: 
        """
        Recover tasks from the storage and execute a callback for each task.
        """
        raise NotImplementedError()
