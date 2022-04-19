from .base import BaseResponse
from pydantic import constr


class UserLoginResponse(BaseResponse):
    status_code = 201
    session_id: constr(min_length=128, max_length=128)
