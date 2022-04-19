from messenger.models.responses.base import BaseResponse


class BaseErrorResponse(BaseResponse):
    message: str
