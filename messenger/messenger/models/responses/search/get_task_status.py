from messenger.models.responses.base import BaseResponse


class GetTaskStatusResponse(BaseResponse):
    status_code = 200
    status: str
