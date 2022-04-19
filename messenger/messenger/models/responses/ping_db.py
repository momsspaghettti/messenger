from .base import BaseResponse


class PingDbResponse(BaseResponse):
    status_code = 200
    message: str = 'Database is available'
