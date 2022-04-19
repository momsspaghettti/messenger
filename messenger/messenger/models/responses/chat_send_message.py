from .base import BaseResponse
from pydantic import constr


class ChatSendMessageResponse(BaseResponse):
    status_code = 201
    message_id: constr(min_length=1)
