from typing import Callable

from wf_airtable_api_client.models.educators import *
from wf_airtable_api_client.models import educators

from . import response as response_models
from . import educators_schools as educators_schools_models
from . import hubs as hubs_models
from . import languages as languages_models
from . import montessori_certifications as montessori_certifications_models
from ..airtable.base_school_db import (
    montessori_certifications as airtable_montessori_certifications_models,
    languages as airtable_languages_models,
    educators as airtable_educator_models,
    educators_schools as airtable_educators_schools_models,
    newsletters as airtable_newsletters_models,
    socio_economic_backgrounds as airtable_socio_economic_backgrounds_models,
)
from ..airtable.base_school_db.languages import CertificationStatus


class CreateUpdateAPIEducatorFields(educators.CreateUpdateAPIEducatorFields):
    def to_airtable_educator(self, exclude_unset=False) -> airtable_educator_models.CreateAirtableEducatorFields:
        from ..airtable.client import AirtableClient
        from ..airtable.base_school_db.field_categories import FieldCategoryType

        airtable_client = AirtableClient()

        record = airtable_educator_models.CreateAirtableEducatorFields()

        # 7/15/2022 - Moved away from Contact Info for a more flat structure in the Educator table itself
        # contact_info = []
        # if contact_info_id:
        #    contact_info.append(contact_info_id)

        if exclude_unset is False or (exclude_unset and "email" in self.model_fields_set):
            record.primary_personal_email = self.email
        if exclude_unset is False or (exclude_unset and "first_name" in self.model_fields_set):
            record.first_name = self.first_name
        if exclude_unset is False or (exclude_unset and "last_name" in self.model_fields_set):
            record.last_name = self.last_name
        if exclude_unset is False or (exclude_unset and "details" in self.model_fields_set):
            record.details = self.details
        if exclude_unset is False or (
            exclude_unset and "initial_interest_in_governance_model" in self.model_fields_set
        ):
            record.initial_interest_in_governance_model = self.initial_interest_in_governance_model
        if exclude_unset is False or (exclude_unset and "stage" in self.model_fields_set):
            record.stage = self.stage
        if exclude_unset is False or (exclude_unset and "home_address" in self.model_fields_set):
            record.home_address = self.home_address
        if exclude_unset is False or (exclude_unset and "status" in self.model_fields_set):
            record.status = self.status
        if exclude_unset is False or (exclude_unset and "individual_type" in self.model_fields_set):
            if self.individual_type == APIEducatorIndividualTypes.COMMUNITY_MEMBER:
                record.individual_type = "Community Member"
            else:
                record.individual_type = "Educator"

        newsletter_ids = []
        newsletter_slugs = []
        if self.discovery_newsletter:
            newsletter_slugs.append(airtable_newsletters_models.NewsletterSlugs.DISCOVERY_GROUP)
        if self.etl_newsletter:
            newsletter_slugs.append(airtable_newsletters_models.NewsletterSlugs.EMERGING_TEACHER_LEADER_GROUP)
        if len(newsletter_slugs) > 0:
            newsletters = airtable_client.get_newsletters_by_slug(newsletter_slugs)
            newsletter_ids = list(map(lambda n: n.id, newsletters.root))

        if exclude_unset is False or (exclude_unset and len(newsletter_ids) > 0):
            record.newsletters = newsletter_ids

        if exclude_unset is False or (exclude_unset and "assigned_partner_id" in self.model_fields_set):
            assigned_partner = None
            if self.assigned_partner_id:
                assigned_partner = [self.assigned_partner_id]
            record.assigned_partner = assigned_partner

        if exclude_unset is False or (exclude_unset and "target_community_id" in self.model_fields_set):
            target_community = None
            if self.target_community_id:
                target_community = [self.target_community_id]
            record.target_community = target_community

        if exclude_unset is False or (exclude_unset and "start_a_school_response_id" in self.model_fields_set):
            start_a_school_response = None
            if self.start_a_school_response_id:
                start_a_school_response = [self.start_a_school_response_id]
            record.ssj_typeforms_start_a_school = start_a_school_response

        if exclude_unset is False or (exclude_unset and "get_involved_response_id" in self.model_fields_set):
            get_involved_response = None
            if self.get_involved_response_id:
                get_involved_response = [self.get_involved_response_id]
            record.ssj_fillout_forms_get_involved = get_involved_response

        age_classrooms_set = set()
        age_classrooms = None
        if self.initial_interest_in_age_classrooms:
            age_classrooms_mapping = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.classroom_levels, self.initial_interest_in_age_classrooms
            )

            for m in age_classrooms_mapping:
                if m["is_custom_value"] is False:
                    age_classrooms_set.add(m["mapped_value"])
            age_classrooms = list(age_classrooms_set)
        record.initial_interest_in_age_classrooms = age_classrooms

        return record

    # 7/15/2022 - Moved away from Contact Info for a more flat structure in the Educator table itself
    # def to_airtable_contact_info(
    #     self, educator_id: Optional[str] = None
    # ) -> airtable_contact_info_models.CreateAirtableContactInfoFields:
    #     educator = []
    #     if educator_id:
    #         educator.append(educator_id)
    #     return airtable_contact_info_models.CreateAirtableContactInfoFields(
    #         educator=educator, type="Personal email", email=self.email, is_primary=True
    #     )

    def to_airtable_socio_economic(
        self, educator_id
    ) -> airtable_socio_economic_backgrounds_models.CreateAirtableSocioEconomicBackgroundFields:
        from ..airtable.client import AirtableClient
        from ..airtable.base_school_db.field_categories import FieldCategoryType

        airtable_client = AirtableClient()

        set_race_and_ethnicity = set()
        set_race_and_ethnicity_other = set()
        race_and_ethnicity = None
        race_and_ethnicity_other = None
        if self.race_and_ethnicity is not None:
            race_and_ethnicity_mapping = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.race_ethnicity, self.race_and_ethnicity
            )

            for m in race_and_ethnicity_mapping:
                if m["is_custom_value"] is True:
                    set_race_and_ethnicity_other.add(m["mapped_value"])
                else:
                    set_race_and_ethnicity.add(m["mapped_value"])

        if len(set_race_and_ethnicity) > 0:
            race_and_ethnicity = list(set_race_and_ethnicity)
        if len(set_race_and_ethnicity_other) > 0:
            race_and_ethnicity_other = ";".join(set_race_and_ethnicity_other)

        educational_attainment = None
        if self.educational_attainment is not None:
            education_mapping = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.educational_attainment, str(self.educational_attainment)
            )
            if len(education_mapping) > 0:
                if not education_mapping[0]["is_custom_value"] is True:
                    educational_attainment = education_mapping[0]["mapped_value"]

        household_income = None
        if self.household_income is not None:
            household_income_mapping = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.household_income, str(self.household_income)
            )
            if len(household_income_mapping) > 0:
                if not household_income_mapping[0]["is_custom_value"] is True:
                    household_income = household_income_mapping[0]["mapped_value"]

        set_gender = set()
        set_gender_other = set()
        gender = None
        gender_other = None
        if self.gender is not None:
            gender_mapping = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.gender, self.gender
            )
            for m in gender_mapping:
                if m["is_custom_value"] is True:
                    set_gender_other.add(m["mapped_value"])
                else:
                    set_gender.add(m["mapped_value"])

        if len(set_gender) > 0:
            gender = list(set_gender)[0]
        if len(set_gender_other) > 0:
            gender_other = ";".join(set_gender_other)

        # TODO: Use Enums
        lgbtqia = None
        if self.lgbtqia_identifying is not None:
            lgbtqia_mapping = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.lgbtqia, str(self.lgbtqia_identifying)
            )
            if len(lgbtqia_mapping) > 0:
                if not lgbtqia_mapping[0]["is_custom_value"] is True:
                    lgbtqia = lgbtqia_mapping[0]["mapped_value"]

        # TODO: Use Enums
        set_pronouns = set()
        set_pronouns_other = set()
        pronouns = None
        pronouns_other = None
        if self.pronouns is not None:
            pronoun_mapping = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.pronouns, self.pronouns
            )
            for m in pronoun_mapping:
                if m["is_custom_value"] is True:
                    set_pronouns_other.add(m["mapped_value"])
                else:
                    set_pronouns.add(m["mapped_value"])

        if len(set_pronouns) > 0:
            pronouns = list(set_pronouns)[0]
        if len(set_pronouns_other) > 0:
            pronouns_other = ";".join(set_pronouns_other)

        return airtable_socio_economic_backgrounds_models.CreateAirtableSocioEconomicBackgroundFields(
            educator=[educator_id],
            race_and_ethnicity=race_and_ethnicity,
            race_and_ethnicity_other=race_and_ethnicity_other,
            educational_attainment=educational_attainment,
            household_income=household_income,
            gender=gender,
            gender_other=gender_other,
            lgbtqia_identifying=lgbtqia,
            pronouns=pronouns,
            pronouns_other=pronouns_other,
        )

    def to_airtable_languages(self, socio_economic_id) -> list[airtable_languages_models.CreateAirtableLanguageFields]:
        from ..airtable.client import AirtableClient
        from ..airtable.base_school_db.field_categories import FieldCategoryType

        airtable_client = AirtableClient()
        airtable_languages = []

        for language in self.languages:
            set_languages = set()
            set_languages_other = set()

            languages_mapping = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.languages, language.language
            )
            for m in languages_mapping:
                if m["is_custom_value"] is True:
                    set_languages_other.add(m["mapped_value"])
                else:
                    if m["mapped_value"].lower() != "other":
                        set_languages.add(m["mapped_value"])

            if len(set_languages) > 0:
                for l in list(set_languages):
                    airtable_language = airtable_languages_models.CreateAirtableLanguageFields(
                        socio_economic_background=[socio_economic_id],
                        language_dropdown=l,
                        language_other=None,
                        is_primary_language=language.is_primary_language,
                    )
                    airtable_languages.append(airtable_language)

            if len(set_languages_other) > 0:
                for l in list(set_languages_other):
                    airtable_language = airtable_languages_models.CreateAirtableLanguageFields(
                        socio_economic_background=[socio_economic_id],
                        language_dropdown="Other",
                        language_other=l,
                        is_primary_language=language.is_primary_language,
                    )
                    airtable_languages.append(airtable_language)

        return airtable_languages

    def to_airtable_montessori_certifications(
        self, educator_id
    ) -> list[airtable_montessori_certifications_models.CreateAirtableMontessoriCertificationFields]:
        from ..airtable.client import AirtableClient
        from ..airtable.base_school_db.field_categories import FieldCategoryType

        airtable_client = AirtableClient()

        airtable_montessori_certifications = []
        for certification in self.montessori_certifications:
            set_certification_levels = set()
            mapped_certification_levels = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.montessori_certification_levels, certification.certification_levels
            )
            for m in mapped_certification_levels:
                if m["is_custom_value"] is True:
                    set_certification_levels.add("Unknown")
                else:
                    set_certification_levels.add(m["mapped_value"])
            certification_levels = list(set_certification_levels)

            mapped_certifiers = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.montessori_certifiers, certification.certifier
            )
            # set_certifier = set()
            # set_certifier_other = set()
            # certifier = None
            # certifier_other = None
            # for m in mapped_certifiers:
            #     if m['is_custom_value'] is True:
            #         set_certifier_other.add(m['mapped_value'])
            #     else:
            #         set_certifier.add(m['mapped_value'])
            # if len(set_certifier) > 0:
            #     certifier = list(set_certifier)
            # if len(set_certifier_other) > 0:
            #     certifier_other = list(set_certifier_other)
            certifier = None
            certifier_other = None
            for m in mapped_certifiers:
                if m["is_custom_value"]:
                    certifier_other = m["mapped_value"]
                else:
                    certifier = m["mapped_value"]

            certification_status = None
            if certification.is_montessori_certified:
                certification_status = CertificationStatus.CERTIFIED
            elif certification.is_seeking_montessori_certification:
                certification_status = CertificationStatus.TRAINING

            airtable_montessori_certification = (
                airtable_montessori_certifications_models.CreateAirtableMontessoriCertificationFields(
                    educator=[educator_id],
                    year_certified=certification.year_certified,
                    certification_levels=certification_levels,
                    certifier=certifier,
                    certifier_other=certifier_other,
                    certification_status=certification_status,
                )
            )
            airtable_montessori_certifications.append(airtable_montessori_certification)

        return airtable_montessori_certifications


class APIEducatorData(educators.APIEducatorData):
    @classmethod
    def from_airtable_educator(
        cls, airtable_educator: airtable_educator_models.AirtableEducatorResponse, url_path_for: Callable
    ):
        fields = APIEducatorFields(
            full_name=airtable_educator.fields.full_name,
            first_name=airtable_educator.fields.first_name,
            last_name=airtable_educator.fields.last_name,
            email=airtable_educator.fields.email,
            all_emails=airtable_educator.fields.all_emails,
            primary_personal_email=airtable_educator.fields.primary_personal_email,
            other_personal_emails=airtable_educator.fields.other_personal_emails,
            primary_wildflower_email=airtable_educator.fields.primary_wildflower_email,
            wildflowerschools_email=airtable_educator.fields.wildflowerschools_email,
            details=airtable_educator.fields.details,
            home_address=airtable_educator.fields.home_address,
            target_community=airtable_educator.fields.target_community_name,
            stage=airtable_educator.fields.stage,
            status=airtable_educator.fields.status,
            visioning_album_complete=airtable_educator.fields.visioning_album_complete,
            visioning_album=airtable_educator.fields.visioning_album,
            current_roles=airtable_educator.fields.current_roles,
            source=airtable_educator.fields.source,
            source_other=airtable_educator.fields.source_other,
            race_and_ethnicity=airtable_educator.fields.race_and_ethnicity,
            race_and_ethnicity_other=airtable_educator.fields.race_and_ethnicity_other,
            educational_attainment=airtable_educator.fields.educational_attainment,
            household_income=airtable_educator.fields.household_income,
            income_background=airtable_educator.fields.income_background,
            gender=airtable_educator.fields.gender,
            lgbtqia_identifying=airtable_educator.fields.lgbtqia_identifying,
            pronouns=airtable_educator.fields.pronouns,
            montessori_certified=airtable_educator.fields.montessori_certified,
            initial_interest_in_governance_model=airtable_educator.fields.initial_interest_in_governance_model,
            discovery_newsletter=any(
                n.fields.slug == airtable_newsletters_models.NewsletterSlugs.DISCOVERY_GROUP.value
                for n in airtable_educator.fields.newsletters
            ),
            etl_newsletter=any(
                n.fields.slug == airtable_newsletters_models.NewsletterSlugs.EMERGING_TEACHER_LEADER_GROUP.value
                for n in airtable_educator.fields.newsletters
            ),
        )

        educators_schools_data = []
        if airtable_educator.fields.educators_schools is not None:
            for d in airtable_educator.fields.educators_schools:
                if isinstance(d, airtable_educators_schools_models.AirtableEducatorsSchoolsResponse):
                    educators_schools_data.append(
                        response_models.APIDataWithFields(
                            id=d.id,
                            type=educators_schools_models.MODEL_TYPE,
                            fields=educators_schools_models.APIEducatorSchoolFields(
                                roles=d.fields.roles,
                                email=d.fields.email,
                                currently_active=d.fields.currently_active,
                                start_date=d.fields.start_date,
                                end_date=d.fields.end_date,
                            ),
                        )
                    )
                else:
                    educators_schools_data.append(d)

        educators_languages_data = []
        if airtable_educator.fields.languages is not None:
            for d in airtable_educator.fields.languages:
                if isinstance(d, airtable_languages_models.AirtableLanguageResponse):
                    educators_languages_data.append(
                        response_models.APIDataWithFields(
                            id=d.id,
                            type=languages_models.MODEL_TYPE,
                            fields=languages_models.APILanguagesFields(
                                full_name=d.fields.educator_full_name,
                                language=d.fields.language,
                                language_dropdown=d.fields.language_dropdown,
                                language_other=d.fields.language_other,
                                is_primary_language=d.fields.is_primary_language,
                            ),
                        )
                    )
                else:
                    educators_languages_data.append(d)

        educators_montessori_certifications_data = []
        if airtable_educator.fields.montessori_certifications is not None:
            for d in airtable_educator.fields.montessori_certifications:
                if isinstance(d, airtable_montessori_certifications_models.AirtableMontessoriCertificationResponse):
                    educators_montessori_certifications_data.append(
                        response_models.APIDataWithFields(
                            id=d.id,
                            type=montessori_certifications_models.MODEL_TYPE,
                            fields=montessori_certifications_models.APIMontessoriCertificationsFields(
                                full_name=d.fields.educator_full_name,
                                year_certified=d.fields.year_certified,
                                certification_levels=d.fields.certification_levels,
                                certifier=d.fields.certifier,
                                certifier_other=d.fields.certifier_other,
                                certification_status=d.fields.certification_status,
                            ),
                        )
                    )
                else:
                    educators_montessori_certifications_data.append(d)

        hub_data = response_models.APILinksAndData()
        if airtable_educator.fields.hub is not None:
            hub_data = response_models.APILinksAndData(
                links={"self": url_path_for("get_hub", hub_id=airtable_educator.fields.hub)},
                data=response_models.APIDataWithFields(
                    id=airtable_educator.fields.hub,
                    type=hubs_models.MODEL_TYPE,
                    fields=hubs_models.APIHubFields(name=airtable_educator.fields.hub_name),
                ),
            )

        relationships = APIEducatorRelationships(
            educators_schools=response_models.APILinksAndData(
                links={"self": url_path_for("get_educator_schools", educator_id=airtable_educator.id)},
                data=educators_schools_data,
            ),
            assigned_partner=response_models.APILinks(
                links={"self": url_path_for("get_educator_guides", educator_id=airtable_educator.id)}
            ),
            languages=response_models.APILinksAndData(links=None, data=educators_languages_data),
            montessori_certifications=response_models.APILinksAndData(
                links=None, data=educators_montessori_certifications_data
            ),
            hub=hub_data,
        )
        links = response_models.APILinks(links={"self": url_path_for("get_educator", educator_id=airtable_educator.id)})
        return cls(
            id=airtable_educator.id, type=MODEL_TYPE, fields=fields, relationships=relationships, links=links.links
        )


class ListAPIEducatorData(educators.ListAPIEducatorData):
    @classmethod
    def from_airtable_educators(
        cls, airtable_educators: airtable_educator_models.ListAirtableEducatorResponse, url_path_for: Callable
    ):
        educator_responses = []
        for e in airtable_educators.root:
            educator_responses.append(
                APIEducatorData.from_airtable_educator(airtable_educator=e, url_path_for=url_path_for)
            )

        return cls(root=educator_responses)
