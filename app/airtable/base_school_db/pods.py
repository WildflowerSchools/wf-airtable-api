from typing import Optional

from pydantic import Field, field_validator, RootModel

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none


class AirtablePodFields(BaseModel):
    name: Optional[str] = Field(None, alias="Name")
    hub: Optional[str] = Field(None, alias="Hub")
    pod_contacts: Optional[list[str]] = Field(None, alias="Pod Contact")
    schools: Optional[list[str]] = Field(None, alias="Schools")

    @field_validator("hub", mode="before")
    def _get_first_or_default_none(cls, v: str) -> Optional[str]:
        return get_first_or_default_none(v)
        # _get_first_or_default_none = validator("hub", pre=True, allow_reuse=True)(get_first_or_default_none)


class AirtablePodResponse(AirtableResponse):
    fields: AirtablePodFields


class ListAirtablePodResponse(RootModel):
    root: list[AirtablePodResponse]
