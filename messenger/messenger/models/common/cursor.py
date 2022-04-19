from messenger.models.base import MyBaseModel
from pydantic import validator


class Cursor(MyBaseModel):
    iterator: str

    @validator('iterator')
    def iterator_must_not_be_empty_or_contain_spaces(cls, v):
        if v is None or v == '' or ' ' in v:
            raise ValueError('"iterator" must not be empty or contain spaces')

        return v
