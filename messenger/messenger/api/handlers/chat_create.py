from .base import BaseView
from messenger.models.requests.chat_create import ChatCreateRequest
from messenger.models.responses.base import BaseResponse
from messenger.models.responses.chat_create import ChatCreateResponse
from typing import Optional
from messenger.models.common.global_user import GlobalUser
from messenger.db.schema import chats_table


class ChatCreateView(BaseView):
    """
    /v1/chats:
    post:
      description: "создать чат с именем chat_name"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: "object"
              properties:
                chat_name:
                  type: string
                  maxLength: 255
                  description: "название для создаваемого чата"
                  example: "новый чат"
      responses:
        '201':
          $ref: '#/components/responses/ChatCreateResponse'
        '400':
          description: |
            * `bad-parameters` - неправильный формат входных параметров
        default:
          $ref: '#/components/responses/DefaultErrorResponse'
    """

    URL_PATH = r'/v1/chats'

    async def post(self):
        """
        создать чат с именем chat_name
        """

        return await self.handle_request(ChatCreateRequest)

    async def process_request(
            self,
            request: ChatCreateRequest,
            user: Optional[GlobalUser],
            db_available: bool) -> BaseResponse:
        chat_create_query = chats_table \
            .insert() \
            .values({'chat_name': request.chat_name}) \
            .returning(chats_table.c.chat_id)

        async with self.db.acquire() as conn:
            async with conn.begin():
                result = await (await conn.execute(
                    chat_create_query
                )).fetchone()
                return ChatCreateResponse(chat_id=result['chat_id'])

    @property
    def can_process_request_without_db(self):
        return False

    @property
    def need_to_auth(self) -> bool:
        return True
