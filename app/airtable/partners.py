from typing import Optional, Union

from pydantic import BaseModel, Field, validator

from .guides_schools import AirtableGuidesSchoolsResponse
from .response import AirtableResponse


class AirtablePartnerFields(BaseModel):
    name: Optional[str] = Field(alias="Name")
    email: Optional[str] = Field(alias="Email")
    active: Optional[str] = Field(alias="Currently active")
    active_stint: Optional[list[str]] = Field(alias="Active stint")
    roles: Optional[list[str]] = Field(alias="Roles")
    hubs: Optional[list[str]] = Field(alias="Hubs")
    pods: Optional[list[str]] = Field(alias="Pods")
    schools_partner_guiding: Optional[list[Union[str, AirtableGuidesSchoolsResponse]]] = Field(alias="Guides x Schools")
    educators_partner_guiding: Optional[list[str]] = Field(alias="TLs")

    @validator("schools_partner_guiding")
    def load_schools_guides_relationship(cls, value):
        from .client import AirtableClient
        airtable_client = AirtableClient()

        loaded_schools_guides = value.copy()
        for ii, school_guide in enumerate(loaded_schools_guides):
            if isinstance(school_guide, str):
                raw = airtable_client.get_guide_school_by_id(school_guide)
                loaded_schools_guides[ii] = AirtableGuidesSchoolsResponse.parse_obj(raw)

        return loaded_schools_guides


class AirtablePartnerResponse(AirtableResponse):
    fields: AirtablePartnerFields


class ListAirtablePartnerResponse(BaseModel):
    __root__: list[AirtablePartnerResponse]
