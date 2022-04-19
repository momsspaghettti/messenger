from .base import BaseRequest
from pydantic import constr


class UserLoginRequest(BaseRequest):
    login: constr(min_length=1, max_length=255)
    password: constr(min_length=1, max_length=255)
