from .chat import ChatRequest
from pydantic import conint, Field, validator
from typing import Optional
from messenger.models.common.cursor import Cursor


class ChatGetMessagesRequest(ChatRequest):
    limit: conint(ge=1, le=1000)
    from_cursor: Optional[Cursor] = Field(alias='from')

    @validator('from_cursor', pre=True)
    def parse_from_field(cls, v):
        if v is None:
            return None

        return {'iterator': v}
