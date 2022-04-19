from .base import BaseResponse


class ChatJoinResponse(BaseResponse):
    status_code = 201
    """id пользователя user_name в чате chat_id, уникальный в рамках этого чата"""
    user_id: str
