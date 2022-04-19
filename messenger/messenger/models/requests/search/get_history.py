from messenger.models.requests.base import BaseRequest
from pydantic import constr


class GetHistoryRequest(BaseRequest):
    message: constr(min_length=4)
