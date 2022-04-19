from typing import Optional
from .base import BaseView
from messenger.models.common.global_user import GlobalUser
from messenger.models.requests.ping import PingRequest
from messenger.models.responses.base import BaseResponse
from messenger.models.responses.ping import PingResponse


class PingView(BaseView):
    URL_PATH = r'/ping'

    async def get(self):
        return await self.handle_request(PingRequest)

    async def process_request(
            self,
            request: PingRequest,
            user: Optional[GlobalUser],
            db_available: bool) -> BaseResponse:
        return PingResponse()

    @property
    def need_to_auth(self) -> bool:
        return False

    @property
    def can_process_request_without_db(self) -> bool:
        return True
