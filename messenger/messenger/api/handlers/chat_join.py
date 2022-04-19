from messenger.models.requests.chat_join import ChatJoinRequest
from messenger.models.responses.chat_join import ChatJoinResponse
from .base import BaseView
from messenger.models.responses.base import BaseResponse
from typing import Optional
from messenger.models.common.global_user import GlobalUser
from messenger.db.schema import chats_users_table as users_tbl
from messenger.db.queries import check_if_chat_exists
from messenger.models.responses.errors.not_found import NotFoundErrorResponse


class ChatJoinView(BaseView):
    """
    /v1/chats/{chat_id}/users:
    post:
      description: "добавить пользователя user_name в чат chat_id"
      parameters:
        - in: path
          required: true
          name: chat_id
          schema:
            type: string
          description: "id чата, полученное при создании чата"
          example: "the-chat-id"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: "object"
              properties:
                user_name:
                  type: string
                  maxLength: 255
                  description: "username пользователя"
                  example: "Vasya Pupkin"
      responses:
        '201':
          $ref: '#/components/responses/ChatJoinResponse'
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

    URL_PATH = r'/v1/chats/{chat_id:\S+}/users'

    async def post(self):
        """
        добавить пользователя user_name в чат chat_id
        """
        return await self.handle_request(ChatJoinRequest)

    async def process_request(
            self,
            request: ChatJoinRequest,
            user: Optional[GlobalUser],
            db_available: bool) -> BaseResponse:
        logger = self.get_logger(__name__)

        async with self.db.acquire() as conn:
            async with conn.begin():
                if not await check_if_chat_exists(conn, request.chat_id, logger):
                    return NotFoundErrorResponse('chat')

                chat_user = {
                    'user_name': request.user_name,
                    'chat_id': request.chat_id,
                    'global_user_id': user.id_
                }

                result = await (await conn.execute(
                    users_tbl.insert().values(chat_user).returning(users_tbl.c.user_id)
                )).fetchone()

                return ChatJoinResponse(user_id=str(result['user_id']))

    @property
    def can_process_request_without_db(self):
        return False

    @property
    def need_to_auth(self) -> bool:
        return True
