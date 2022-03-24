from typing import Optional, Union

from pydantic import BaseModel, Field, validator

from app.airtable.base_school_db import guides_schools as airtable_guides_schools_models
from app.airtable.response import AirtableResponse


# noinspection PyMethodParameters
class AirtablePartnerFields(BaseModel):
    name: Optional[str] = Field(alias="Name")
    email: Optional[str] = Field(alias="Email")
    active: Optional[str] = Field(alias="Currently active")
    active_stint: Optional[list[str]] = Field(alias="Active stint")
    roles: Optional[list[str]] = Field(alias="Roles")
    hubs: Optional[list[str]] = Field(alias="Hubs")
    pods: Optional[list[str]] = Field(alias="Pods")
    schools_partner_guiding: Optional[list[Union[str, airtable_guides_schools_models.AirtableGuidesSchoolsResponse]]] = Field(
        alias="Guides x Schools")
    educators_partner_guiding: Optional[list[str]] = Field(alias="TLs")

    @validator("schools_partner_guiding")
    def load_schools_guides_relationship(cls, value):
        from ..client import AirtableClient
        airtable_client = AirtableClient()

        schools_guides = value.copy()
        _ids = []
        _records = []
        for id_or_record in schools_guides:
            if isinstance(id_or_record, airtable_guides_schools_models.AirtableGuidesSchoolsResponse):
                _records.append(id_or_record)
            elif isinstance(id_or_record, str):
                _ids.append(id_or_record)

        list_airtable_guides_schools = airtable_client.list_guide_schools_by_ids(guide_school_ids=_ids)
        _records += list_airtable_guides_schools.__root__

        return _records


class AirtablePartnerResponse(AirtableResponse):
    fields: AirtablePartnerFields


class ListAirtablePartnerResponse(BaseModel):
    __root__: list[AirtablePartnerResponse]
