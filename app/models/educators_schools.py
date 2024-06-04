from typing import Callable

from wf_airtable_api_schema.models.educators_schools import *
from wf_airtable_api_schema.models import educators_schools

from . import response as response_models
from . import educators as educators_models
from . import schools as schools_models
from ..airtable.base_school_db import (
    educators as airtable_educator_models,
    schools as airtable_school_models,
    educators_schools as airtable_educator_school_models,
)


class CreateUpdateAPIEducatorSchoolFields(educators_schools.CreateUpdateAPIEducatorSchoolFields):
    def to_airtable_educator_schools(
        self,
    ) -> airtable_educator_school_models.CreateUpdateAirtableEducatorsSchoolsFields:
        return airtable_educator_school_models.CreateUpdateAirtableEducatorsSchoolsFields(
            educator=[self.educator_id],
            school=[self.school_id],
            email=self.email,
            roles=self.roles,
            currently_active=self.currently_active,
            start_date=self.start_date,
            end_date=self.end_date,
            mark_for_deletion=self.mark_for_deletion,
        )


class APIEducatorSchoolData(educators_schools.APIEducatorSchoolData):
    @classmethod
    def from_airtable_educator_school(
        cls,
        airtable_educator_school: airtable_educator_school_models.AirtableEducatorsSchoolsResponse,
        url_path_for: Callable,
    ):
        fields = APIEducatorSchoolFields(
            start_date=airtable_educator_school.fields.start_date,
            end_date=airtable_educator_school.fields.end_date,
            email=airtable_educator_school.fields.email,
            roles=airtable_educator_school.fields.roles,
            currently_active=airtable_educator_school.fields.currently_active,
            mark_for_deletion=airtable_educator_school.fields.mark_for_deletion,
        )

        educator_record = airtable_educator_school.fields.educator
        educator_id = educator_record
        educator_data = educator_record
        if isinstance(educator_record, airtable_educator_models.AirtableEducatorResponse):
            educator_id = educator_record.id
            educator_data = response_models.APIDataWithFields(
                id=educator_record.id,
                type=educators_models.MODEL_TYPE,
                fields=educators_models.APIEducatorMetaFields.parse_obj(educator_record.fields),
            )

        school_record = airtable_educator_school.fields.school
        school_id = school_record
        school_data = school_record
        if isinstance(school_record, airtable_school_models.AirtableSchoolResponse):
            school_id = school_record.id
            school_data = response_models.APIDataWithFields(
                id=school_record.id,
                type=schools_models.MODEL_TYPE,
                fields=schools_models.APISchoolMetaFields.parse_obj(school_record.fields),
            )

        relationships = APIEducatorSchoolRelationships(
            educator=response_models.APILinksAndData(
                links={"self": url_path_for("get_educator", educator_id=educator_id)},
                data=educator_data,
            ),
            school=response_models.APILinksAndData(
                links={"self": url_path_for("get_school", school_id=school_id)},
                data=school_data,
            ),
        )

        links = response_models.APILinks(
            links={"self": url_path_for("get_educator_school", educator_school_id=airtable_educator_school.id)}
        )

        return cls(
            id=airtable_educator_school.id,
            type=MODEL_TYPE,
            fields=fields,
            relationships=relationships,
            links=links.links,
        )


class ListAPIEducatorSchoolData(educators_schools.ListAPIEducatorSchoolData):
    @classmethod
    def from_airtable_educator_schools(
        cls,
        airtable_educator_schools: airtable_educator_school_models.ListAirtableEducatorsSchoolsResponse,
        url_path_for: Callable,
    ):
        responses = []
        for es in airtable_educator_schools.root:
            responses.append(
                APIEducatorSchoolData.from_airtable_educator_school(
                    airtable_educator_school=es, url_path_for=url_path_for
                )
            )

        return cls(root=responses)
