from datetime import datetime

from pydantic import BaseModel


class AirtableResponse(BaseModel):
    id: str
    fields: dict
    createdTime: datetime


class ListAirtableResponse(BaseModel):
    __root__: list[AirtableResponse]
