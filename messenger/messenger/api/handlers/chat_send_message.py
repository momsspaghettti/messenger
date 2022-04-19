from .base import BaseView
from messenger.models.requests.chat_send_message import ChatSendMessageRequest
from messenger.models.responses.base import BaseResponse
from messenger.models.responses.chat_send_message import ChatSendMessageResponse
from typing import Optional
from messenger.models.common.global_user import GlobalUser
from messenger.models.responses.errors.bad_default import DefaultErrorResponse
from messenger.utils.messages_cache import MessagesCache
from messenger.db.queries import check_if_chat_exists, check_if_chat_user_exists
from messenger.models.responses.errors.not_found import NotFoundErrorResponse
from messenger.db.schema import chats_messages_table as messages_tbl


class ChatSendMessageView(BaseView):
    """
    /v1/chats/{chat_id}/messages:
    post:
      description: "отправить в чат chat_id сообщение message"
      parameters:
        - in: path
          required: true
          name: chat_id
          schema:
            type: string
          example: "the-chat-id"
        - in: query
          required: true
          name: user_id
          schema:
            type: string
          example: "the-user-id"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: "object"
              properties:
                message:
                  type: string
                  description: "текст сообщения"
                  example: "Hello"
      responses:
        '201':
          $ref: '#/components/responses/ChatSendMessageResponse'
        '400':
          description: |
            * `bad-parameters` - неправильный формат входных параметров
        '404':
          description: |
            * `chat-not-found` - указанный чат не существует
            * `user-not-found` - в указанном чате нет указанного пользователя
        default:
          $ref: '#/components/responses/DefaultErrorResponse'
    """

    async def process_request(
            self,
            request: ChatSendMessageRequest,
            user: Optional[GlobalUser],
            db_available: bool) -> BaseResponse:
        if not db_available:
            return DefaultErrorResponse(message='Database is unavailable')

        logger = self.get_logger(__name__)

        async with self.db.acquire() as conn:
            async with conn.begin():
                if not await check_if_chat_exists(conn, request.chat_id, logger):
                    return NotFoundErrorResponse('chat')

                if not await check_if_chat_user_exists(conn, request.user_id, request.chat_id, logger):
                    return NotFoundErrorResponse('user')

                message = {
                    'msg': request.message,
                    'chat_id': request.chat_id,
                    'from_chat_user': request.user_id
                }

                result = await (await conn.execute(
                    messages_tbl.insert(message).returning(messages_tbl.c.message_id)
                )).fetchone()

                self.cache.invalidate(request.chat_id)

                return ChatSendMessageResponse(message_id=result['message_id'])

    @property
    def cache(self) -> MessagesCache:
        return self.request.app['messages_cache']

    @property
    def can_process_request_without_db(self) -> bool:
        return False

    @property
    def need_to_auth(self) -> bool:
        return True
