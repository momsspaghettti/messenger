from .base import BaseResponse


class UserRegisterResponse(BaseResponse):
    status_code = 201
    message: str = 'user registered'
