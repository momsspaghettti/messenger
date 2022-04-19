from .base import BaseResponse


class UserLogoutResponse(BaseResponse):
    status_code = 201
    message: str = 'user logged out'
