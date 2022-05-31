from typing import Optional

from pydantic import Field

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse, ListAirtableResponse


class AirtableHubFields(BaseModel):
    name: Optional[str] = Field(alias="Name")
    regional_site_entrepreneurs: Optional[list[str]] = Field(alias="Regional entrepreneur")
    pods: Optional[list[str]] = Field(alias="Pod Assignments")
    schools: Optional[list[str]] = Field(alias="Schools")


class AirtableHubResponse(AirtableResponse):
    fields: AirtableHubFields


class ListAirtableHubResponse(ListAirtableResponse):
    __root__: list[AirtableHubResponse]
