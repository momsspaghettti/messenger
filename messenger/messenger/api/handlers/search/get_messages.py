from typing import Optional
from messenger.models.common.global_user import GlobalUser
from messenger.models.requests.search.get_messages import HistoryGetMessagesRequest
from messenger.models.responses.base import BaseResponse
from .base import BaseChatsSearchView
from messenger.models.responses.errors.not_found import NotFoundErrorResponse
from messenger.models.responses.errors.bad_default import DefaultErrorResponse
from asyncio import Task
from typing import List
from messenger.models.common.history_message import HistoryMessage
from messenger.models.responses.errors.bad_params import BadParametersResponse
from messenger.models.responses.search.get_messages import HistoryGetMessagesResponse
from messenger.models.common.cursor import Cursor


class HistoryGetMessagesView(BaseChatsSearchView):
    URL_PATH = r'/v1/chats/search/{task_id:\S+}/messages'

    async def get(self):
        return await self.handle_request(HistoryGetMessagesRequest)

    async def process_request(
            self,
            request: HistoryGetMessagesRequest,
            user: Optional[GlobalUser],
            db_available: bool) -> BaseResponse:
        if request.task_id not in self.search_tasks:
            return NotFoundErrorResponse('task')

        task: Task = self.search_tasks[request.task_id]

        if task is None:
            return NotFoundErrorResponse('task')

        if not task.done() or task.exception() is not None:
            return NotFoundErrorResponse('task')

        await task
        result: List[HistoryMessage] = task.result()

        if result is None:
            return DefaultErrorResponse()

        from_ = 0 if request.from_cursor is None else int(request.from_cursor.iterator)
        limit = request.limit

        if from_ > len(result):
            return BadParametersResponse()

        response = HistoryGetMessagesResponse(messages=result[from_:from_ + limit])
        if from_ + limit < len(result):
            response.next = Cursor(iterator=str(from_ + limit))

        return response
