from abc import ABC, abstractmethod
from typing import Any


class IStateStorage(ABC):
    @abstractmethod
    async def save_state(self, user_id: str, state: dict[str, Any]) -> None:
        """
        Save the state for a given user.
        """
        raise NotImplementedError()

    @abstractmethod
    async def load_state(self, user_id: str) -> dict[str, Any]:
        """
        Load the state for a given user.
        """
        raise NotImplementedError()

    @abstractmethod
    async def clear_state(self, user_id: str) -> None:
        """
        Clear the state for a given user.
        """
        raise NotImplementedError()
