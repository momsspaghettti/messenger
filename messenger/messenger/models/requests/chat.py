from .base import BaseRequest
from pydantic import validator


class ChatRequest(BaseRequest):
    chat_id: str

    @validator('chat_id')
    def chat_id_must_not_be_empty_or_contain_spaces(cls, v):
        if v is None or v == '' or ' ' in v:
            raise ValueError('"chat_id" must not be empty or contain spaces')

        return v
