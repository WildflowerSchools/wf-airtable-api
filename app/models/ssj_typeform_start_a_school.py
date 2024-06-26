from datetime import datetime
from typing import Callable

from wf_airtable_api_client.models.ssj_typeform_start_a_school import *
from wf_airtable_api_client.models import ssj_typeform_start_a_school

from ..airtable.base_school_db import typeform_start_a_school as airtable_start_a_school_models


class CreateApiSSJTypeformStartASchoolFields(ssj_typeform_start_a_school.CreateApiSSJTypeformStartASchoolFields):
    def to_airtable(self) -> airtable_start_a_school_models.CreateAirtableSSJTypeformStartASchool:
        montessori_certification_levels = None
        if self.montessori_certification_levels is not None:
            montessori_certification_levels = ", ".join(self.montessori_certification_levels)

        age_classrooms_interested_in_offering = None
        if self.age_classrooms_interested_in_offering is not None:
            age_classrooms_interested_in_offering = ", ".join(self.age_classrooms_interested_in_offering)

        socio_economic_race_and_ethnicity = None
        if self.socio_economic_race_and_ethnicity is not None:
            socio_economic_race_and_ethnicity = ", ".join(self.socio_economic_race_and_ethnicity)

        entry_date = datetime.now()
        if self.entry_date is not None:
            entry_date = self.entry_date

        return airtable_start_a_school_models.CreateAirtableSSJTypeformStartASchool(
            educator=[self.educator_id],
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            is_montessori_certified=self.is_montessori_certified,
            is_seeking_montessori_certification=self.is_seeking_montessori_certification,
            montessori_certification_certifier=self.montessori_certification_certifier,
            montessori_certification_year=self.montessori_certification_year,
            montessori_certification_levels=montessori_certification_levels,
            school_location_city=self.school_location_city,
            school_location_state=self.school_location_state,
            school_location_country=self.school_location_country,
            school_location_community=self.school_location_community,
            contact_location_city=self.contact_location_city,
            contact_location_state=self.contact_location_state,
            contact_location_country=self.contact_location_country,
            has_interest_in_joining_another_school=self.has_interest_in_joining_another_school,
            is_willing_to_move=self.is_willing_to_move,
            is_interested_in_charter=self.is_interested_in_charter,
            age_classrooms_interested_in_offering=age_classrooms_interested_in_offering,
            socio_economic_race_and_ethnicity=socio_economic_race_and_ethnicity,
            socio_economic_race_and_ethnicity_other=self.socio_economic_race_and_ethnicity_other,
            socio_economic_lgbtqia_identifying=(
                str(self.socio_economic_lgbtqia_identifying) if self.socio_economic_lgbtqia_identifying else None
            ),
            socio_economic_pronouns=self.socio_economic_pronouns,
            socio_economic_pronouns_other=self.socio_economic_pronouns_other,
            socio_economic_gender=self.socio_economic_gender,
            socio_economic_gender_other=self.socio_economic_gender_other,
            socio_economic_household_income=self.socio_economic_household_income,
            socio_economic_primary_language=self.socio_economic_primary_language,
            message=self.message,
            equity_reflection=self.equity_reflection,
            receive_communications=self.receive_communications,
            source=self.source,
            entry_date=entry_date,
        )


class ApiSSJTypeformStartASchoolData(ssj_typeform_start_a_school.ApiSSJTypeformStartASchoolData):
    @classmethod
    def from_airtable(
        cls,
        airtable_start_a_school: airtable_start_a_school_models.AirtableSSJTypeformStartASchoolResponse,
        url_path_for: Callable,
    ):
        montessori_certification_levels = None
        if airtable_start_a_school.fields.montessori_certification_levels is not None:
            montessori_certification_levels = [
                mcl.strip() for mcl in airtable_start_a_school.fields.montessori_certification_levels.split(", ")
            ]

        age_classrooms = None
        if airtable_start_a_school.fields.age_classrooms_interested_in_offering is not None:
            age_classrooms = [
                ac.strip() for ac in airtable_start_a_school.fields.age_classrooms_interested_in_offering.split(", ")
            ]

        socio_economic_race_and_ethnicity = None
        if airtable_start_a_school.fields.socio_economic_race_and_ethnicity is not None:
            socio_economic_race_and_ethnicity = [
                re.strip() for re in airtable_start_a_school.fields.socio_economic_race_and_ethnicity.split(", ")
            ]

        educator_id = None
        if (
            isinstance(airtable_start_a_school.fields.educator, list)
            and len(airtable_start_a_school.fields.educator) > 0
        ):
            educator_id = airtable_start_a_school.fields.educator[0]

        fields = ApiSSJTypeformStartASchoolFields(
            educator_id=educator_id,
            response_id=airtable_start_a_school.fields.response_id,
            first_name=airtable_start_a_school.fields.first_name,
            last_name=airtable_start_a_school.fields.last_name,
            email=airtable_start_a_school.fields.email,
            is_montessori_certified=airtable_start_a_school.fields.is_montessori_certified,
            is_seeking_montessori_certification=airtable_start_a_school.fields.is_seeking_montessori_certification,
            montessori_certification_certifier=airtable_start_a_school.fields.montessori_certification_certifier,
            montessori_certification_year=airtable_start_a_school.fields.montessori_certification_year,
            montessori_certification_levels=montessori_certification_levels,
            school_location_city=airtable_start_a_school.fields.school_location_city,
            school_location_state=airtable_start_a_school.fields.school_location_state,
            school_location_country=airtable_start_a_school.fields.school_location_country,
            school_location_community=airtable_start_a_school.fields.school_location_community,
            contact_location_city=airtable_start_a_school.fields.contact_location_city,
            contact_location_state=airtable_start_a_school.fields.contact_location_state,
            contact_location_country=airtable_start_a_school.fields.contact_location_country,
            has_interest_in_joining_another_school=airtable_start_a_school.fields.has_interest_in_joining_another_school,
            is_willing_to_move=airtable_start_a_school.fields.is_willing_to_move,
            is_interested_in_charter=airtable_start_a_school.fields.is_interested_in_charter,
            age_classrooms_interested_in_offering=age_classrooms,
            socio_economic_race_and_ethnicity=socio_economic_race_and_ethnicity,
            socio_economic_race_and_ethnicity_other=airtable_start_a_school.fields.socio_economic_race_and_ethnicity_other,
            socio_economic_lgbtqia_identifying=airtable_start_a_school.fields.socio_economic_lgbtqia_identifying,
            socio_economic_pronouns=airtable_start_a_school.fields.socio_economic_pronouns,
            socio_economic_pronouns_other=airtable_start_a_school.fields.socio_economic_pronouns_other,
            socio_economic_gender=airtable_start_a_school.fields.socio_economic_gender,
            socio_economic_gender_other=airtable_start_a_school.fields.socio_economic_gender_other,
            socio_economic_household_income=airtable_start_a_school.fields.socio_economic_household_income,
            socio_economic_primary_language=airtable_start_a_school.fields.socio_economic_primary_language,
            message=airtable_start_a_school.fields.message,
            equity_reflection=airtable_start_a_school.fields.equity_reflection,
            receive_communications=airtable_start_a_school.fields.receive_communications,
            source=airtable_start_a_school.fields.source,
            entry_date=airtable_start_a_school.fields.entry_date,
        )

        return cls(id=airtable_start_a_school.id, type=MODEL_TYPE, fields=fields, relationships={}, links={})
