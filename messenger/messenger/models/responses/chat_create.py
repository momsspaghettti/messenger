from .base import BaseResponse


class ChatCreateResponse(BaseResponse):
    status_code = 201
    chat_id: str
