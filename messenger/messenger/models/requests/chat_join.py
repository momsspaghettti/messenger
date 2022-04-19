from .chat import ChatRequest
from pydantic import constr


class ChatJoinRequest(ChatRequest):
    user_name: constr(min_length=1, max_length=255)
