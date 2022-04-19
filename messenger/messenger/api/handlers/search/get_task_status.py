from typing import Optional
from messenger.models.common.global_user import GlobalUser
from messenger.models.requests.search.get_task_status import GetTaskStatusRequest
from messenger.models.responses.base import BaseResponse
from .base import BaseChatsSearchView
from messenger.models.responses.search.get_task_status import GetTaskStatusResponse
from messenger.models.responses.errors.not_found import NotFoundErrorResponse
from asyncio import Task


class GetTaskStatusView(BaseChatsSearchView):
    URL_PATH = r'/v1/chats/search/status/{task_id:\S+}'

    async def get(self):
        return await self.handle_request(GetTaskStatusRequest)

    async def process_request(
            self,
            request: GetTaskStatusRequest,
            user: Optional[GlobalUser],
            db_available: bool) -> BaseResponse:
        if request.task_id not in self.search_tasks:
            return NotFoundErrorResponse('task')

        task: Task = self.search_tasks[request.task_id]

        if not task.done() and not task.cancelled():
            return GetTaskStatusResponse(status='IN_PROCESS')

        if task.cancelled() or task.exception() is not None:
            return GetTaskStatusResponse(status='FAILED')

        if task.done() and task.exception() is None:
            return GetTaskStatusResponse(status='SUCCESS')

        return GetTaskStatusResponse(status='WAITING')
