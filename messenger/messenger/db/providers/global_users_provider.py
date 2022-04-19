from messenger.models.common.global_user import GlobalUser
from abc import ABC, abstractmethod
from typing import List, Optional


class GlobalUsersProvider(ABC):
    @abstractmethod
    async def save_users(self, users: List[GlobalUser]) -> None:
        raise NotImplementedError('abstract method')

    @abstractmethod
    async def get_user(self, login: str) -> Optional[GlobalUser]:
        raise NotImplementedError('abstract method')
