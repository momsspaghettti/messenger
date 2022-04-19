from typing import Optional
from .base import BaseView
from messenger.models.common.global_user import GlobalUser
from messenger.models.responses.base import BaseResponse
from messenger.models.requests.user_logout import UserLogoutRequest
from messenger.models.responses.user_logout import UserLogoutResponse
from messenger.db.schema import users_sessions_table as sessions_tbl


class UserLogoutView(BaseView):
    URL_PATH = r'/v1/logout'

    async def post(self):
        return await self.handle_request(UserLogoutRequest)

    async def process_request(
            self,
            request: UserLogoutRequest,
            user: Optional[GlobalUser],
            db_available: bool) -> BaseResponse:
        delete_session_query = sessions_tbl \
            .delete() \
            .where(sessions_tbl.c.global_user_id == user.id_)

        async with self.db.acquire() as conn:
            await conn.execute(delete_session_query)

        return UserLogoutResponse()

    @property
    def need_to_auth(self) -> bool:
        return True

    @property
    def can_process_request_without_db(self) -> bool:
        return False
