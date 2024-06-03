from datetime import datetime
from typing import Any

from pydantic import RootModel, field_validator

from app.airtable.base_model import BaseModel


class AirtableResponse(BaseModel):
    id: str
    fields: dict
    createdTime: datetime

    @field_validator("fields", mode="before")
    @classmethod
    def transform_relationships(cls, v: Any):
        return dict(v)


class ListAirtableResponse(RootModel):
    root: list[AirtableResponse]
