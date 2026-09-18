from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.model.user import User

class UserRepositoryPort(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def list_users(self, skip: int = 0, limit: int = 50) -> List[User]:
        pass
