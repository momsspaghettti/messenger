from .base import BaseErrorResponse


class DefaultErrorResponse(BaseErrorResponse):
    status_code = 500
    message = 'Internal Server Error'
