from .base import BaseResponse


class PingResponse(BaseResponse):
    status_code = 200
    message: str = 'OK'
