from datetime import datetime
from typing import Callable

from wf_airtable_api_schema.models.ssj_fillout_get_involved import *
from wf_airtable_api_schema.models import ssj_fillout_get_involved

from ..airtable.base_school_db import fillout_get_involved as airtable_fillout_get_involved


class CreateApiSSJFilloutGetInvolvedFields(ssj_fillout_get_involved.CreateApiSSJFilloutGetInvolvedFields):
    def to_airtable(self) -> ssj_fillout_get_involved.CreateApiSSJFilloutGetInvolvedFields:
        age_classrooms_interested_in_offering = None
        if self.age_classrooms_interested_in_offering is not None:
            age_classrooms_interested_in_offering = ", ".join(self.age_classrooms_interested_in_offering)

        educator_interests = None
        if self.educator_interests is not None:
            educator_interests = ", ".join(self.educator_interests)

        socio_economic_race_and_ethnicity = None
        if self.socio_economic_race_and_ethnicity is not None:
            socio_economic_race_and_ethnicity = ", ".join(self.socio_economic_race_and_ethnicity)

        entry_date = datetime.now()
        if self.entry_date is not None:
            entry_date = self.entry_date

        return airtable_fillout_get_involved.CreateAirtableSSJFilloutGetInvolved(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            contact_type=self.contact_type,
            is_montessori_certified=self.is_montessori_certified,
            is_seeking_montessori_certification=self.is_seeking_montessori_certification,
            montessori_certification_certifier_1=self.montessori_certification_certifier_1,
            montessori_certification_year_1=self.montessori_certification_year_1,
            montessori_certification_level_1=self.montessori_certification_level_1,
            montessori_certification_certifier_2=self.montessori_certification_certifier_2,
            montessori_certification_year_2=self.montessori_certification_year_2,
            montessori_certification_level_2=self.montessori_certification_level_2,
            montessori_certification_certifier_3=self.montessori_certification_certifier_3,
            montessori_certification_year_3=self.montessori_certification_year_3,
            montessori_certification_level_3=self.montessori_certification_level_3,
            montessori_certification_certifier_4=self.montessori_certification_certifier_4,
            montessori_certification_year_4=self.montessori_certification_year_4,
            montessori_certification_level_4=self.montessori_certification_level_4,
            city=self.city,
            state=self.state,
            country=self.country,
            age_classrooms_interested_in_offering=age_classrooms_interested_in_offering,
            educator_interests=educator_interests,
            educator_interests_other=self.educator_interests_other,
            community_member_interest=self.community_member_interest,
            community_member_support_finding_teachers=self.community_member_support_finding_teachers,
            community_member_community_info=self.community_member_community_info,
            community_member_self_info=self.community_member_self_info,
            socio_economic_race_and_ethnicity=socio_economic_race_and_ethnicity,
            socio_economic_race_and_ethnicity_other=self.socio_economic_race_and_ethnicity_other,
            socio_economic_pronouns=self.socio_economic_pronouns,
            socio_economic_pronouns_other=self.socio_economic_pronouns_other,
            socio_economic_gender=self.socio_economic_gender,
            socio_economic_gender_other=self.socio_economic_gender_other,
            socio_economic_household_income=self.socio_economic_household_income,
            socio_economic_primary_language=self.socio_economic_primary_language,
            socio_economic_primary_language_other=self.socio_economic_primary_language_other,
            message=self.message,
            receive_communications=self.receive_communications,
            source=self.source,
            entry_date=entry_date,
        )


class ApiSSJFilloutGetInvolvedData(ssj_fillout_get_involved.ApiSSJFilloutGetInvolvedData):
    @classmethod
    def from_airtable(
        cls,
        airtable_get_involved: airtable_fillout_get_involved.AirtableSSJFilloutGetInvolvedResponse,
        url_path_for: Callable,
    ):
        educator_interests = None
        if airtable_get_involved.fields.educator_interests is not None:
            educator_interests = [ei.strip() for ei in airtable_get_involved.fields.educator_interests.split(', ')]

        age_classrooms = None
        if airtable_get_involved.fields.age_classrooms_interested_in_offering is not None:
            age_classrooms = [ac.strip() for ac in airtable_get_involved.fields.age_classrooms_interested_in_offering.split(', ')]

        socio_economic_race_and_ethnicity = None
        if airtable_get_involved.fields.socio_economic_race_and_ethnicity is not None:
            socio_economic_race_and_ethnicity = [
                re.strip() for re in airtable_get_involved.fields.socio_economic_race_and_ethnicity.split(', ')
            ]

        fields = ApiSSJFilloutGetInvolvedFields(
            response_id=airtable_get_involved.fields.response_id,
            first_name=airtable_get_involved.fields.first_name,
            last_name=airtable_get_involved.fields.last_name,
            email=airtable_get_involved.fields.email,
            contact_type=airtable_get_involved.fields.contact_type,
            is_montessori_certified=airtable_get_involved.fields.is_montessori_certified,
            is_seeking_montessori_certification=airtable_get_involved.fields.is_seeking_montessori_certification,
            montessori_certification_certifier_1=airtable_get_involved.fields.montessori_certification_certifier_1,
            montessori_certification_year_1=airtable_get_involved.fields.montessori_certification_year_1,
            montessori_certification_level_1=airtable_get_involved.fields.montessori_certification_level_1,
            montessori_certification_certifier_2=airtable_get_involved.fields.montessori_certification_certifier_2,
            montessori_certification_year_2=airtable_get_involved.fields.montessori_certification_year_2,
            montessori_certification_level_2=airtable_get_involved.fields.montessori_certification_level_2,
            montessori_certification_certifier_3=airtable_get_involved.fields.montessori_certification_certifier_3,
            montessori_certification_year_3=airtable_get_involved.fields.montessori_certification_year_3,
            montessori_certification_level_3=airtable_get_involved.fields.montessori_certification_level_3,
            montessori_certification_certifier_4=airtable_get_involved.fields.montessori_certification_certifier_4,
            montessori_certification_year_4=airtable_get_involved.fields.montessori_certification_year_4,
            montessori_certification_level_4=airtable_get_involved.fields.montessori_certification_level_4,
            city=airtable_get_involved.fields.city,
            state=airtable_get_involved.fields.state,
            country=airtable_get_involved.fields.country,
            age_classrooms_interested_in_offering=age_classrooms,
            educator_interests=educator_interests,
            educator_interests_other=airtable_get_involved.fields.educator_interests_other,
            community_member_interest=airtable_get_involved.fields.community_member_interest,
            community_member_support_finding_teachers=airtable_get_involved.fields.community_member_support_finding_teachers,
            community_member_community_info=airtable_get_involved.fields.community_member_community_info,
            community_member_self_info=airtable_get_involved.fields.community_member_self_info,
            socio_economic_race_and_ethnicity=socio_economic_race_and_ethnicity,
            socio_economic_race_and_ethnicity_other=airtable_get_involved.fields.socio_economic_race_and_ethnicity_other,
            socio_economic_pronouns=airtable_get_involved.fields.socio_economic_pronouns,
            socio_economic_pronouns_other=airtable_get_involved.fields.socio_economic_pronouns_other,
            socio_economic_gender=airtable_get_involved.fields.socio_economic_gender,
            socio_economic_gender_other=airtable_get_involved.fields.socio_economic_gender_other,
            socio_economic_household_income=airtable_get_involved.fields.socio_economic_household_income,
            socio_economic_primary_language=airtable_get_involved.fields.socio_economic_primary_language,
            socio_economic_primary_language_other=airtable_get_involved.fields.socio_economic_primary_language_other,
            message=airtable_get_involved.fields.message,
            receive_communications=airtable_get_involved.fields.receive_communications,
            source=airtable_get_involved.fields.source,
            entry_date=airtable_get_involved.fields.entry_date,
        )

        return cls(id=airtable_get_involved.id, type=MODEL_TYPE, fields=fields, relationships={}, links={})
