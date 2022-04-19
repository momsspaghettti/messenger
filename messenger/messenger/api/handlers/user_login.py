from typing import Optional
from .base import BaseView
from messenger.models.common.global_user import GlobalUser
from messenger.models.responses.base import BaseResponse
from messenger.models.requests.user_login import UserLoginRequest
from messenger.models.responses.errors.not_found import NotFoundErrorResponse
from messenger.models.responses.errors.unauthorized import UnauthorizedErrorResponse
from messenger.models.responses.user_login import UserLoginResponse
from messenger.utils.crypto import is_correct_password, compute_session_id
from messenger.db.schema import (
    global_users_table as global_users_tbl,
    users_sessions_table as sessions_tbl)
from sqlalchemy import select


class UserLoginView(BaseView):
    URL_PATH = r'/v1/login'

    async def post(self):
        return await self.handle_request(UserLoginRequest)

    async def process_request(
            self,
            request: UserLoginRequest,
            _: Optional[GlobalUser],
            db_available: bool) -> BaseResponse:

        user_and_session_query = select(
            global_users_tbl.c.id,
            global_users_tbl.c.password_hash_sha512,
            sessions_tbl.c.session_id
        ) \
            .outerjoin(sessions_tbl, global_users_tbl.c.id == sessions_tbl.c.global_user_id) \
            .where(global_users_tbl.c.login == request.login)

        async with self.db.acquire() as conn:
            async with conn.begin():
                user_and_session_select = await conn.execute(
                    user_and_session_query
                )

                if user_and_session_select.rowcount != 1:
                    return NotFoundErrorResponse('user')

                global_user_and_session = await user_and_session_select.fetchone()
                password_hash = global_user_and_session['password_hash_sha512']

                if not is_correct_password(request.password, password_hash):
                    return UnauthorizedErrorResponse(message='login or password is incorrect')

                session_id = global_user_and_session['session_id']
                if session_id is None:
                    session_id = (await (await conn.execute(
                        sessions_tbl.insert().values({
                            'session_id': compute_session_id(request.login, password_hash),
                            'global_user_id': global_user_and_session['id']
                        }).returning(sessions_tbl.c.session_id)
                    )).fetchone())['session_id']

                return UserLoginResponse(session_id=session_id)

    @property
    def need_to_auth(self) -> bool:
        return False

    @property
    def can_process_request_without_db(self) -> bool:
        return False
