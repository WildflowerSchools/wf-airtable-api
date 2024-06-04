from typing import Optional

from pydantic import ConfigDict, Field

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse

MODEL_TYPE = "contact_info"


class CreateAirtableContactInfoFields(BaseModel):
    educator: Optional[list[str]] = Field(None, alias="Educator")
    type: Optional[str] = Field(None, alias="Type")
    email: Optional[str] = Field(None, alias="Email")
    phone: Optional[str] = Field(None, alias="Phone")
    is_primary: Optional[bool] = Field(alias="Primary", default=False)
    model_config = ConfigDict(populate_by_name=True)


class AirtableContactInfoFields(CreateAirtableContactInfoFields):
    pass


class AirtableContactInfoResponse(AirtableResponse):
    fields: AirtableContactInfoFields
