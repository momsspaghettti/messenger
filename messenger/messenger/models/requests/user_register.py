from .base import BaseRequest
from pydantic import constr, conint
from typing import Optional


class UserRegisterRequest(BaseRequest):
    login: constr(min_length=1, max_length=255)
    password: constr(min_length=1, max_length=255)
    user_name: constr(min_length=1, max_length=255)
    utc_offset: Optional[conint(ge=-24, le=24)]
