from typing import Optional, Union

from pydantic import BaseModel, Field, validator

from app.airtable.base_school_db import guides_schools as airtable_guides_schools_models
from app.airtable.response import AirtableResponse


class AirtablePartnerFields(BaseModel):
    synced_record_id: Optional[str] = Field(alias="Synced Record ID")
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

    def load_schools_guides_relationship(self):
        from ..client import AirtableClient
        airtable_client = AirtableClient()

        _ids = []
        _records = []
        for id_or_record in self.schools_partner_guiding:
            if isinstance(id_or_record, airtable_guides_schools_models.AirtableGuidesSchoolsResponse):
                _records.append(id_or_record)
            elif isinstance(id_or_record, str):
                _ids.append(id_or_record)

        list_airtable_guides_schools = airtable_client.list_guide_schools_by_ids(guide_school_ids=_ids)
        _records += list_airtable_guides_schools.__root__

        self.schools_partner_guiding = _records
        return _records

    def load_relationships(self):
        self.load_schools_guides_relationship()


class AirtablePartnerResponse(AirtableResponse):
    fields: AirtablePartnerFields

    def load_relationships(self):
        self.fields.load_relationships()


class ListAirtablePartnerResponse(BaseModel):
    __root__: list[AirtablePartnerResponse]

    def load_relationships(self):
        for r in self.__root__:
            r.load_relationships()
