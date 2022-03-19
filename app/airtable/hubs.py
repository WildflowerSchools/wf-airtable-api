from typing import Optional

from pydantic import BaseModel, Field

from .response import AirtableResponse


class AirtableHubFields(BaseModel):
    name: Optional[str] = Field(alias="Name")
    regional_site_entrepreneurs: Optional[list[str]] = Field(alias="Regional entrepreneur")
    pods: Optional[list[str]] = Field(alias="Pod Assignments")
    schools: Optional[list[str]] = Field(alias="Schools")


class AirtableHubResponse(AirtableResponse):
    fields: AirtableHubFields


class ListAirtableHubResponse(BaseModel):
    __root__: list[AirtableHubResponse]
