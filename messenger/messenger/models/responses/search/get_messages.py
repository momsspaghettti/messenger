from messenger.models.responses.base import BaseResponse
from typing import List, Optional
from messenger.models.common.history_message import HistoryMessage
from messenger.models.common.cursor import Cursor


class HistoryGetMessagesResponse(BaseResponse):
    status_code = 200
    messages: List[HistoryMessage]
    next: Optional[Cursor]
