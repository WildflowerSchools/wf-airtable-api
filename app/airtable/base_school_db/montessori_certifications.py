from typing import Optional

from pydantic import Field, validator

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none


class CreateAirtableMontessoriCertificationFields(BaseModel):
    educator: Optional[list[str]] = Field(alias="Educator")
    year_certified: Optional[int] = Field(alias="Year Certified")
    certification_levels: Optional[list[str]] = Field(alias="Certification Levels")
    certifier: Optional[str] = Field(alias="Certifier")
    certifier_other: Optional[str] = Field(alias="Certifier - Other")
    certification_status: Optional[str] = Field(alias="Certification Status")

    class Config:
        allow_population_by_field_name = True


class AirtableMontessoriCertificationFields(CreateAirtableMontessoriCertificationFields):
    educator_full_name: Optional[str] = Field(alias="Educator Full Name")

    _get_first_or_default_none = validator("educator_full_name", pre=True, allow_reuse=True)(get_first_or_default_none)


class AirtableMontessoriCertificationResponse(AirtableResponse):
    fields: AirtableMontessoriCertificationFields


class ListAirtableMontessoriCertificationResponse(BaseModel):
    __root__: list[AirtableMontessoriCertificationResponse]
