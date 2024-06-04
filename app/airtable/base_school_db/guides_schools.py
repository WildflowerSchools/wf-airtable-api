from datetime import date
from typing import Optional, Union

from pydantic import Field, field_validator, RootModel

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none


class AirtableGuidesSchoolsFields(BaseModel):
    school_id: Optional[str] = Field(None, alias="School")
    guide_id: Optional[str] = Field(None, alias="Guide or Entrepreneur")
    start_date: Optional[date] = Field(None, alias="Start date")
    end_date: Optional[date] = Field(None, alias="End date")
    type: Optional[str] = Field(None, alias="Type")
    active: Optional[bool] = Field(None, alias="Currently active")

    @field_validator("school_id", "guide_id", mode="before")
    def _get_first_or_default_none(cls, v: Union[str, int, float]) -> Optional[Union[str, int, float]]:
        return get_first_or_default_none(v)

    # _get_first_or_default_none = validator("school_id", "guide_id", pre=True, allow_reuse=True)(
    #     get_first_or_default_none
    # )


class AirtableGuidesSchoolsResponse(AirtableResponse):
    fields: AirtableGuidesSchoolsFields


class ListAirtableGuidesSchoolsResponse(RootModel):
    root: list[AirtableGuidesSchoolsResponse]
