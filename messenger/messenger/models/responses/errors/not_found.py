from .base import BaseErrorResponse


class NotFoundErrorResponse(BaseErrorResponse):
    status_code = 404

    def __init__(self, prefix: str):
        super().__init__(message=prefix + '-not-found')
