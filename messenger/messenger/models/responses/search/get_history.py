from messenger.models.responses.base import BaseResponse


class GetHistoryResponse(BaseResponse):
    status_code = 201
    task_id: str
