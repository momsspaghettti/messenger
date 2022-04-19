from .base import BaseRequest
from pydantic import constr


class ChatCreateRequest(BaseRequest):
    chat_name: constr(min_length=1, max_length=255)
