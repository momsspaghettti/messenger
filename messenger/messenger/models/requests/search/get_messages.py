from messenger.models.requests.base import BaseRequest
from pydantic import constr, conint, Field, validator
from typing import Optional
from messenger.models.common.cursor import Cursor


class HistoryGetMessagesRequest(BaseRequest):
    task_id: constr(min_length=1)
    limit: conint(ge=1, le=100)
    from_cursor: Optional[Cursor] = Field(alias='from')

    @validator('from_cursor', pre=True)
    def parse_from_field(cls, v):
        if v is None:
            return None

        return {'iterator': v}
