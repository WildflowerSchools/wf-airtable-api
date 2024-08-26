from typing import Optional

from pydantic import Field

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse, ListAirtableResponse


class AirtableHubFields(BaseModel):
    name: Optional[str] = Field(None, alias="Name")
    regional_site_entrepreneurs: Optional[list[str]] = Field(None, alias="Regional entrepreneur")
    # pods: Optional[list[str]] = Field(None, alias="Pod Assignments")
    schools: Optional[list[str]] = Field(None, alias="Schools")


class AirtableHubResponse(AirtableResponse):
    fields: AirtableHubFields


class ListAirtableHubResponse(ListAirtableResponse):
    root: list[AirtableHubResponse]
