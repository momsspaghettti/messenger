from .base import BaseResponse
from pydantic import conlist
from messenger.models.common.message import Message
from typing import Optional
from messenger.models.common.cursor import Cursor


class ChatGetMessagesResponse(BaseResponse):
    status_code = 200
    messages: conlist(Message, max_items=1000)
    next: Optional[Cursor]
