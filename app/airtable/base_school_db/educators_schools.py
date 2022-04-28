from datetime import date
from typing import Optional, Union

from pydantic import BaseModel, Field, validator


from . import educators as educators_models
from . import schools as schools_models
from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none


class CreateUpdateAirtableEducatorsSchoolsFields(BaseModel):
    educator: Optional[list[str]] = Field(alias="Educator")
    school: Optional[list[str]] = Field(alias="School")

    roles: Optional[list[str]] = Field(alias="Roles (staging)")
    currently_active: Optional[bool] = Field(alias="Currently Active")
    start_date: Optional[date] = Field(alias="Start Date")
    end_date: Optional[date] = Field(alias="End Date")
    mark_for_deletion: Optional[bool] = Field(alias="Mark for deletion")

    class Config:
        allow_population_by_field_name = True


class AirtableFindEducatorsSchoolsFields(CreateUpdateAirtableEducatorsSchoolsFields):
    educator_id: Optional[list[str]] = Field(alias="Educator Record ID")
    school_id: Optional[list[str]] = Field(alias="School Record ID")


class AirtableEducatorsSchoolsFields(CreateUpdateAirtableEducatorsSchoolsFields):
    educator: Optional[Union[str, object]] = Field(alias="Educator")
    school: Optional[Union[str, object]] = Field(alias="School")

    _get_first_or_default_none = validator("educator", "school", pre=True, allow_reuse=True)(get_first_or_default_none)

    def load_educator_relationship(self):
        from ..client import AirtableClient

        airtable_client = AirtableClient()

        if self.educator is None:
            return None

        _record = None
        _id = None
        if isinstance(self.educator, educators_models.AirtableEducatorResponse):
            _record = self.educator
        elif isinstance(self.educator, str):
            _id = self.educator

        if _record is None:
            airtable_educator = airtable_client.get_educator_by_id(educator_id=_id, load_relationships=False)
            _record = airtable_educator

        self.educator = _record
        return _record

    def load_school_relationship(self):
        from ..client import AirtableClient

        airtable_client = AirtableClient()

        if self.school is None:
            return None

        _record = None
        _id = None
        if isinstance(self.school, schools_models.AirtableSchoolResponse):
            _record = self.school
        elif isinstance(self.school, str):
            _id = self.school

        if _record is None:
            airtable_school = airtable_client.get_school_by_id(school_id=_id)
            _record = airtable_school

        self.school = _record
        return _record

    def load_relationships(self):
        self.load_educator_relationship()
        self.load_school_relationship()


class AirtableEducatorsSchoolsResponse(AirtableResponse):
    fields: AirtableEducatorsSchoolsFields

    def load_relationships(self):
        self.fields.load_relationships()


class ListAirtableEducatorsSchoolsResponse(BaseModel):
    __root__: list[AirtableEducatorsSchoolsResponse]

    def load_relationships(self):
        for r in self.__root__:
            r.load_relationships()
