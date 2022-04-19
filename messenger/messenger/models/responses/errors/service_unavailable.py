from .base import BaseErrorResponse


class ServiceUnavailableErrorResponse(BaseErrorResponse):
    status_code = 503
