from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, validator

from .response import AirtableResponse
from .validators import get_first_or_default_none


class AirtableEducatorsSchoolsFields(BaseModel):
    educator_id: Optional[str] = Field(alias="Educator")
    school_id: Optional[str] = Field(alias="School")
    educator_name: Optional[str] = Field(alias="Educator Full Name")
    school_name: Optional[str] = Field(alias="School Name")
    role: Optional[list[str]] = Field(alias="Role")
    currently_active: Optional[bool] = Field(alias="Currently Active")
    start_date: Optional[date] = Field(alias="Start date")
    end_date: Optional[date] = Field(alias="End date")

    _get_first_or_default_none = validator("educator_id", "educator_name", "school_id", "school_name", pre=True,
                                           allow_reuse=True)(get_first_or_default_none)


class AirtableEducatorsSchoolsResponse(AirtableResponse):
    fields: AirtableEducatorsSchoolsFields


class ListAirtableEducatorsSchoolsResponse(BaseModel):
    __root__: list[AirtableEducatorsSchoolsResponse]
