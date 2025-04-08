from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from schema.data_schema import UserHistoryResponseModel


class UserHistoryRepositoryMeta(ABC):
    """
    Abstract base class that defines the interface for User History repositories.
    All concrete User History repository implementations should inherit from this class
    and implement all abstract methods.
    """

    @abstractmethod
    async def get_all(self) -> List[UserHistoryResponseModel]:
        """
        Retrieve all user history records.

        Returns:
            List[UserHistoryResponseModel]: A list of all user history entries
        """
        pass

    @abstractmethod
    async def get_one(self, user_id: UUID) -> Optional[UserHistoryResponseModel]:
        """
        Retrieve user history for a specific user.

        Args:
            user_id (UUID): The ID of the user whose history to retrieve

        Returns:
            Optional[UserHistoryResponseModel]: The user's history if found, None otherwise
        """
        pass

    @abstractmethod
    async def add_one(
        self, user_input: str, response_content: str, user_id: UUID
    ) -> UserHistoryResponseModel:
        """
        Add a new user history entry.

        Args:
            user_input (str): The input provided by the user
            response_content (str): The response content generated for the user
            user_id (UUID): The ID of the user to associate the history with

        Returns:
            UserHistoryResponseModel: The newly created user history entry
        """
        pass
