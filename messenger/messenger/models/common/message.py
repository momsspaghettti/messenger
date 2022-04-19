from messenger.models.base import MyBaseModel


class Message(MyBaseModel):
    text: str
