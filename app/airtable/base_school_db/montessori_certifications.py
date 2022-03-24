from typing import Optional

from pydantic import BaseModel, Field, validator

from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none


class AirtableMontessoriCertificationFields(BaseModel):
    educator_id: Optional[str] = Field(alias="Educator")
    full_name: Optional[str] = Field(alias="Full Name")
    year_certified: Optional[int] = Field(alias="Year Certified")
    certification_levels: Optional[list[str]] = Field(alias="Certification Levels")
    certifier: Optional[str] = Field(alias="Certifier")
    certifier_other: Optional[str] = Field(alias="Certifier - Other")
    certification_status: Optional[str] = Field(alias="Certification Status")

    _get_first_or_default_none = validator("educator_id", "full_name", pre=True,
                                           allow_reuse=True)(get_first_or_default_none)


class AirtableMontessoriCertificationResponse(AirtableResponse):
    fields: AirtableMontessoriCertificationFields


class ListAirtableMontessoriCertificationResponse(BaseModel):
    __root__: list[AirtableMontessoriCertificationResponse]
