from pydantic import BaseModel, Extra


class MyBaseModel(BaseModel):
    """
    Base data model
    """

    class Config:
        validate_assignment = True
        extra: Extra = Extra.forbid
