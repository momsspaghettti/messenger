from .base import BaseErrorResponse


class UnauthorizedErrorResponse(BaseErrorResponse):
    status_code = 401
