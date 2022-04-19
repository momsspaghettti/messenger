from .chat import ChatRequest
from pydantic import validator


class ChatSendMessageRequest(ChatRequest):
    user_id: str
    message: str

    @validator('user_id')
    def user_id_must_not_be_empty_or_contain_spaces(cls, v):
        if v is None or v == '' or ' ' in v:
            raise ValueError('"user_id" must not be empty or contain spaces')

        return v
