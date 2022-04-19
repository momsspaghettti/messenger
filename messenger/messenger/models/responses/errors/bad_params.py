from .base import BaseErrorResponse


class BadParametersResponse(BaseErrorResponse):
    status_code = 400
    message = 'bad-parameters'
