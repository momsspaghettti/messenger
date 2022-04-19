from .chat_send_message import ChatSendMessageView
from .chat_get_messages import ChatGetMessagesView
from .base import Handler
from messenger.models.requests.chat_send_message import ChatSendMessageRequest
from messenger.models.requests.chat_get_messages import ChatGetMessagesRequest


class ChatMessagesView(Handler):
    URL_PATH = r'/v1/chats/{chat_id:\S+}/messages'

    async def post(self):
        """
        отправить в чат chat_id сообщение message
        """
        handler = ChatSendMessageView(self.request)
        return await handler.handle_request(ChatSendMessageRequest)

    async def get(self):
        """
        получить список сообщений из чата chat_id
        """
        handler = ChatGetMessagesView(self.request)
        return await handler.handle_request(ChatGetMessagesRequest)
