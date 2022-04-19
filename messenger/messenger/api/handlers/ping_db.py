from typing import Optional
from .base import BaseView
from messenger.models.common.global_user import GlobalUser
from messenger.models.responses.base import BaseResponse
from messenger.models.requests.ping_db import PingDbRequest
from messenger.models.responses.ping_db import PingDbResponse
from messenger.models.responses.errors.service_unavailable import ServiceUnavailableErrorResponse


class PingDbView(BaseView):
    """
    /v1/ping_db:
    get:
      description: "проверить доступность БД"
      responses:
        '200':
          $ref: '#/components/responses/PingDbResponse'
        '503':
          description: |
            * `db-unavailable` - база данных не доступна
          $ref: '#/components/responses/DefaultErrorResponse'
        default:
          $ref: '#/components/responses/DefaultErrorResponse'
    """

    URL_PATH = r'/ping_db'

    async def get(self):
        return await self.handle_request(PingDbRequest)

    async def process_request(
            self,
            request: PingDbRequest,
            _: Optional[GlobalUser],
            db_available: bool) -> BaseResponse:
        if db_available:
            return PingDbResponse()
        return ServiceUnavailableErrorResponse(message='Database is unavailable')

    @property
    def can_process_request_without_db(self) -> bool:
        return True

    @property
    def need_to_auth(self) -> bool:
        return False
