from abc import ABC, abstractmethod


class AbstractTaskStorageRepository(ABC):
    @abstractmethod
    async def add_task(self) -> None:
        """
        Append a task to the storage.
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def delete_task(self) -> None:
        """
        Delete a task from the storage by its job ID.
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def get_task(self) -> list: 
        """
        Get current task from the storage.
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def recover_tasks(self, callback) -> None: 
        """
        Recover tasks from the storage and execute a callback for each task.
        """
        raise NotImplementedError()
