from typing import Dict, List, Optional
from messenger.models.common.message import Message


class MessageSlot:
    def __init__(self, message: Message, iterator: str):
        self.message: Message = message
        self.iterator: str = iterator


class MessagesCache:
    def __init__(self):
        self.cache: Dict[str, Dict[str, List[MessageSlot]]] = {}
        self.start_cursor_name = 'internal_private_start_cursor'

    def add(self, chat_id: str, from_: str, messages: List[MessageSlot]):
        if chat_id not in self.cache:
            self.cache[chat_id] = {}

        self.cache[chat_id][from_] = messages

    def add_from_start(self, chat_id: str, messages: List[MessageSlot]):
        self.add(chat_id, self.start_cursor_name, messages)

    def invalidate(self, chat_id: str):
        if chat_id in self.cache:
            del self.cache[chat_id]

    def get(self, chat_id: str, from_: str, limit: int) -> (bool, Optional[List[MessageSlot]]):
        if chat_id not in self.cache:
            return False, None
        if from_ not in self.cache[chat_id]:
            return False, None
        messages = self.cache[chat_id][from_]
        return True, messages[:limit]

    def get_from_start(self, chat_id: str, limit: int) -> (bool, Optional[List[MessageSlot]]):
        return self.get(chat_id, self.start_cursor_name, limit)
