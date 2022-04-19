from messenger.models.base import MyBaseModel
from pydantic import constr, conint, Field


class GlobalUser(MyBaseModel):
    id_: int = Field(alias='id')
    session_id: constr(min_length=128, max_length=128)
    login: constr(min_length=1, max_length=255)
    name: constr(min_length=1, max_length=255)
    utc_offset: conint(ge=-24, le=24)
