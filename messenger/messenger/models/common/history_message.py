from messenger.models.base import MyBaseModel


class HistoryMessage(MyBaseModel):
    text: str
    chat_id: str
