from messenger.models.requests.base import BaseRequest
from pydantic import constr


class GetTaskStatusRequest(BaseRequest):
    task_id: constr(min_length=1)
