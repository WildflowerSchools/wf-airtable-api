from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, validator

from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none


class AirtableGuidesSchoolsFields(BaseModel):
    school_id: Optional[str] = Field(alias="School")
    guide_id: Optional[str] = Field(alias="Guide or Entrepreneur")
    start_date: Optional[date] = Field(alias="Start date")
    end_date: Optional[date] = Field(alias="End date")
    type: Optional[str] = Field(alias="Type")
    active: Optional[str] = Field(alias="Currently active")

    _get_first_or_default_none = validator("school_id", "guide_id", pre=True,
                                           allow_reuse=True)(get_first_or_default_none)


class AirtableGuidesSchoolsResponse(AirtableResponse):
    fields: AirtableGuidesSchoolsFields


class ListAirtableGuidesSchoolsResponse(BaseModel):
    __root__: list[AirtableGuidesSchoolsResponse]
