from .base import Handler
from .chat_create import ChatCreateView
from .chat_messages import ChatMessagesView
from .chat_join import ChatJoinView
from typing import List, Type
from .ping_db import PingDbView
from .ping import PingView
from .user_register import UserRegisterView
from .user_login import UserLoginView
from .user_logout import UserLogoutView
from messenger.api.handlers.search.get_history import GetHistoryView
from messenger.api.handlers.search.get_task_status import GetTaskStatusView
from messenger.api.handlers.search.get_messages import HistoryGetMessagesView

HANDLERS: List[Type[Handler]] = [
    ChatMessagesView,
    ChatJoinView,
    ChatCreateView,
    PingDbView,
    PingView,
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    GetHistoryView,
    GetTaskStatusView,
    HistoryGetMessagesView
]
