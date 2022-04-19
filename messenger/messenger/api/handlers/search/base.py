from typing import Optional
from messenger.api.handlers.base import BaseView
from messenger.models.common.global_user import GlobalUser
from messenger.models.requests.base import BaseRequest
from messenger.models.responses.base import BaseResponse
from abc import ABC, abstractmethod
from typing import Dict
from asyncio import Task
import datetime


class BaseChatsSearchView(BaseView, ABC):
    @abstractmethod
    async def process_request(
            self,
            request: BaseRequest,
            user: Optional[GlobalUser],
            db_available: bool) -> BaseResponse:
        raise NotImplementedError('abstract method')

    @property
    def need_to_auth(self) -> bool:
        return True

    @property
    def can_process_request_without_db(self) -> bool:
        return False

    @property
    def search_tasks(self) -> Dict[str, Task]:
        return self.request.app['search_tasks']

    @staticmethod
    def generate_task_id(session_id: str) -> str:
        return session_id + str(datetime.datetime.now().timestamp())
