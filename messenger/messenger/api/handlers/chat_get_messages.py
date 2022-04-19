from messenger.models.responses.base import BaseResponse
from messenger.models.responses.chat_get_messages import ChatGetMessagesResponse
from messenger.models.requests.chat_get_messages import ChatGetMessagesRequest
from messenger.models.responses.errors.not_found import NotFoundErrorResponse
from .base import BaseView
from messenger.models.common.message import Message
from messenger.models.common.cursor import Cursor
from typing import Optional, List
from messenger.models.common.global_user import GlobalUser
from messenger.utils.time import get_good_part_of_day
from messenger.utils.messages_cache import MessagesCache, MessageSlot
from messenger.db.schema import chats_messages_table as messages_tbl
from messenger.db.queries import check_if_chat_exists


class ChatGetMessagesView(BaseView):
    """
    /v1/chats/{chat_id}/messages:
    get:
      description: "получить список сообщений из чата chat_id"
      parameters:
        - in: path
          required: true
          name: chat_id
          schema:
            type: string
          example: "the-chat-id"
        - in: query
          required: true
          name: limit
          schema:
            type: integer
            minimum: 1
            maximum: 1000
          description: "не больше стольки сообщений хотим получить в ответе"
          example: 10
        - in: query
          name: from
          schema:
            $ref: '#/components/schemas/Cursor'
          description: "указатель для сервера, обозначающий место, с которого стоит продолжить получение сообщений;
          если не указан, то сервер должен вернуть limit сообщений, начиная с самого первого сообщения в чате"
      responses:
        '200':
          $ref: '#/components/responses/ChatGetMessagesResponse'
        '400':
          description: |
            * `bad-parameters` - неправильный формат входных параметров
        '404':
          description: |
            * `chat-not-found` - указанный чат не существует
        default:
          $ref: '#/components/responses/DefaultErrorResponse'
    """

    async def process_request(
            self,
            request: ChatGetMessagesRequest,
            user: Optional[GlobalUser],
            db_available: bool) -> BaseResponse:
        if not db_available:
            return ChatGetMessagesResponse(messages=[self.get_bot_message_about_db(user)], next=None)

        logger = self.get_logger(__name__)

        found_in_cache, cache_response = self.get_from_cache_if_found(request)
        if found_in_cache:
            return cache_response

        messages_select_query = messages_tbl \
            .select() \
            .where(messages_tbl.c.chat_id == request.chat_id)
        if request.from_cursor is not None:
            messages_select_query = messages_select_query \
                .where(messages_tbl.c.message_id >= request.from_cursor.iterator)
        messages_select_query = messages_select_query \
            .order_by(messages_tbl.c.message_id) \
            .limit(request.limit + 1)

        async with self.db.acquire() as conn:
            async with conn.begin():
                if not await check_if_chat_exists(conn, request.chat_id, logger):
                    return NotFoundErrorResponse('chat')

                messages: List[MessageSlot] = \
                    [
                        MessageSlot(Message(text=row['msg']), str(row['message_id']))
                        async for row in conn.execute(messages_select_query)]
                if request.from_cursor is not None:
                    self.cache.add(request.chat_id, request.from_cursor.iterator, messages)
                else:
                    self.cache.add_from_start(request.chat_id, messages)

                return self.get_response_for_messages(messages, request.limit)

    def get_from_cache_if_found(self, request: ChatGetMessagesRequest) -> (bool, Optional[ChatGetMessagesResponse]):
        found_in_cache, messages = self.cache.get(
            request.chat_id,
            request.from_cursor.iterator,
            request.limit + 1) \
            if request.from_cursor is not None \
            else \
            self.cache.get_from_start(request.chat_id, request.limit + 1)

        if not found_in_cache:
            return False, None

        return True, self.get_response_for_messages(messages, request.limit)

    @staticmethod
    def get_response_for_messages(messages: List[MessageSlot], limit: int) -> ChatGetMessagesResponse:
        if len(messages) == limit + 1:
            return ChatGetMessagesResponse(
                messages=[message_slot.message for message_slot in messages[:limit]],
                next=Cursor(iterator=messages[-1].iterator))
        return ChatGetMessagesResponse(
            messages=[message_slot.message for message_slot in messages],
            next=None)

    @staticmethod
    def get_bot_message_about_db(user: Optional[GlobalUser]) -> Message:
        greeting: str
        if user is None:
            greeting = 'Привет друг'
        else:
            greeting = f'{get_good_part_of_day(user.utc_offset)}, {user}'
        return Message(text=f'{greeting}. В данный момент сервис находится в состоянии подъема. '
                            'Попробуй вернуться через несколько минут.')

    @property
    def cache(self) -> MessagesCache:
        return self.request.app['messages_cache']

    @property
    def can_process_request_without_db(self):
        return True

    @property
    def need_to_auth(self) -> bool:
        return True
