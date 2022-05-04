from typing import Optional

from pydantic import BaseModel, Field

from app.airtable.response import AirtableResponse

MODEL_TYPE = "contact_info"


class CreateAirtableContactInfoFields(BaseModel):
    educator: Optional[list[str]] = Field(alias="Educator")
    type: Optional[str] = Field(alias="Type")
    email: Optional[str] = Field(alias="Email")
    phone: Optional[str] = Field(alias="Phone")
    is_primary: Optional[bool] = Field(alias="Primary", default=False)

    class Config:
        allow_population_by_field_name = True


class AirtableContactInfoFields(CreateAirtableContactInfoFields):
    pass


class AirtableContactInfoResponse(AirtableResponse):
    fields: AirtableContactInfoFields
