from typing import Optional

from pydantic import BaseModel, Field, validator

from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none


class AirtablePodFields(BaseModel):
    name: Optional[str] = Field(alias="Name")
    hub: Optional[str] = Field(alias="Hub")
    pod_contacts: Optional[list[str]] = Field(alias="Pod Contact")
    schools: Optional[list[str]] = Field(alias="Schools")

    _get_first_or_default_none = validator("hub", pre=True, allow_reuse=True)(get_first_or_default_none)


class AirtablePodResponse(AirtableResponse):
    fields: AirtablePodFields


class ListAirtablePodResponse(BaseModel):
    __root__: list[AirtablePodResponse]
