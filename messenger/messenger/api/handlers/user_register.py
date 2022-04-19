from typing import Optional
from .base import BaseView
from messenger.models.common.global_user import GlobalUser
from messenger.models.requests.user_register import UserRegisterRequest
from messenger.models.responses.base import BaseResponse
from messenger.models.responses.user_register import UserRegisterResponse
from messenger.db.schema import global_users_table as users_tbl
from messenger.utils.crypto import compute_sha512_hash
from messenger.models.responses.errors.bad_params import BadParametersResponse


class UserRegisterView(BaseView):
    URL_PATH = '/v1/register'

    async def post(self):
        return await self.handle_request(UserRegisterRequest)

    async def process_request(
            self,
            request: UserRegisterRequest,
            _: Optional[GlobalUser],
            db_available: bool) -> BaseResponse:
        password_hash = compute_sha512_hash(request.password)

        user = {
            'login': request.login,
            'password_hash_sha512': password_hash,
            'name': request.user_name,
        }

        if request.utc_offset is not None:
            user['utc_offset'] = request.utc_offset

        async with self.db.acquire() as conn:
            async with conn.begin():
                user_with_same_login_select = await conn.execute(
                    users_tbl.select().where(users_tbl.c.login == request.login)
                )

                if user_with_same_login_select.rowcount != 0:
                    return BadParametersResponse(message='user with given login already exists')

                await conn.execute(users_tbl.insert().values(user))
                return UserRegisterResponse()

    @property
    def need_to_auth(self) -> bool:
        return False

    @property
    def can_process_request_without_db(self) -> bool:
        return False
