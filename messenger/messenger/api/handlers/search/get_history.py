import asyncio
from messenger.models.common.global_user import GlobalUser
from messenger.models.responses.base import BaseResponse
from .base import BaseChatsSearchView
from messenger.models.requests.search.get_history import GetHistoryRequest
from messenger.models.responses.search.get_history import GetHistoryResponse
from aiopg.sa.engine import Engine
from typing import List
from messenger.models.common.history_message import HistoryMessage
from messenger.db.schema import (
    chats_messages_table as messages_tbl,
    global_users_table as global_users_tbl,
    chats_users_table as chats_users_tbl)
from sqlalchemy import select
from messenger.utils.timer import Timer


class GetHistoryView(BaseChatsSearchView):
    URL_PATH = r'/v1/chats/search'

    async def post(self):
        return await self.handle_request(GetHistoryRequest)

    async def process_request(
            self,
            request: GetHistoryRequest,
            user: GlobalUser,
            db_available: bool) -> BaseResponse:
        task_id = self.generate_task_id(user.session_id)
        self.search_tasks[task_id] = asyncio.create_task(search_messages(
            self.db,
            user.id_,
            request.message,
            Timer(self.get_logger(__name__), 'search messages history')))
        return GetHistoryResponse(task_id=task_id)


async def search_messages(
        db: Engine,
        global_user_id: int,
        search_text: str,
        timer: Timer) -> List[HistoryMessage]:
    query = select(
        global_users_tbl.c.id.label('global_user_id'),
        chats_users_tbl.c.user_id.label('chat_user_id'),
        messages_tbl.c.chat_id,
        messages_tbl.c.msg
    ) \
        .outerjoin(
        chats_users_tbl,
        global_users_tbl.c.id == chats_users_tbl.c.global_user_id
    ) \
        .outerjoin(
        messages_tbl,
        chats_users_tbl.c.chat_id == messages_tbl.c.chat_id
    ) \
        .where(global_users_tbl.c.id == global_user_id) \
        .where(messages_tbl.c.msg.ilike(f'%{search_text}%')) \
        .order_by(messages_tbl.c.message_id.desc()) \
        .limit(100)

    async with timer:
        async with db.acquire() as conn:
            return [
                HistoryMessage(
                    text=row['msg'],
                    chat_id=row['chat_id']
                ) async for row in conn.execute(query)
            ]
