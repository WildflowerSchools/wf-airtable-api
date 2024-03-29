from typing import Callable

from wf_airtable_api_schema.models.educators import *
from wf_airtable_api_schema.models import educators

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


class CreateAPIEducatorFields(educators.CreateAPIEducatorFields):
    def to_airtable_educator(
        self,  # , contact_info_id: Optional[str] = None
    ) -> airtable_educator_models.CreateAirtableEducatorFields:
        from ..airtable.client import AirtableClient

        airtable_client = AirtableClient()

        # 7/15/2022 - Moved away from Contact Info for a more flat structure in the Educator table itself
        # contact_info = []
        # if contact_info_id:
        #    contact_info.append(contact_info_id)

        newsletter_ids = []
        newsletter_slugs = []
        if self.discovery_newsletter:
            newsletter_slugs.append(airtable_newsletters_models.NewsletterSlugs.DISCOVERY_GROUP)
        if self.etl_newsletter:
            newsletter_slugs.append(airtable_newsletters_models.NewsletterSlugs.EMERGING_TEACHER_LEADER_GROUP)
        if len(newsletter_slugs) > 0:
            newsletters = airtable_client.get_newsletters_by_slug(newsletter_slugs)
            newsletter_ids = list(map(lambda n: n.id, newsletters.__root__))

        assigned_partner = None
        if self.assigned_partner_id:
            assigned_partner = [self.assigned_partner_id]

        target_community = None
        if self.target_community_id:
            target_community = [self.target_community_id]

        start_a_school_response = None
        if self.start_a_school_response_id:
            start_a_school_response = [self.start_a_school_response_id]

        return airtable_educator_models.CreateAirtableEducatorFields(
            primary_personal_email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            details=self.details,
            initial_interest_in_governance_model=self.initial_interest_in_governance_model,
            stage=self.stage,
            home_address=self.home_address,
            assigned_partner=assigned_partner,
            target_community=target_community,
            ssj_typeforms_start_a_school=start_a_school_response,
            newsletters=newsletter_ids,
        )

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

        race_and_ethnicity = None
        race_and_ethnicity_other = None
        if self.race_and_ethnicity is not None:
            (
                race_and_ethnicity,
                race_and_ethnicity_includes_non_specific_category,
            ) = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.race_ethnicity, self.race_and_ethnicity
            )

            if race_and_ethnicity_includes_non_specific_category:
                race_and_ethnicity_other = ";".join(self.race_and_ethnicity)

        educational_attainment = None
        if self.educational_attainment is not None:
            education_categories, _ = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.educational_attainment, str(self.educational_attainment)
            )
            if len(education_categories) > 0:
                educational_attainment = education_categories[0]

        household_income = None
        if self.household_income is not None:
            income_categories, _ = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.household_income, str(self.household_income)
            )
            if len(income_categories) > 0:
                household_income = income_categories[0]

        gender = None
        gender_other = None
        if self.gender is not None:
            genders, gender_includes_non_specific_category = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.gender, self.gender
            )
            if len(genders) > 0:
                gender = genders[0]
            if gender_includes_non_specific_category:
                gender_other = self.gender

        # TODO: Use Enums
        lgbtqia = None
        if self.lgbtqia_identifying is not None:
            lgbtqia_categories, _ = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.lgbtqia, str(self.lgbtqia_identifying)
            )

            if len(lgbtqia_categories) > 0:
                lgbtqia = lgbtqia_categories[0]

        # TODO: Use Enums
        pronouns = None
        pronouns_other = None
        if self.pronouns is not None:
            _pronouns, pronouns_includes_non_specific_category = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.pronouns, self.pronouns
            )
            if len(_pronouns) > 0:
                pronouns = _pronouns[0]
            if pronouns_includes_non_specific_category:
                pronouns_other = self.pronouns

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
        for l in self.languages:
            languages, language_includes_non_specific_category = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.languages, l.language
            )
            language = None
            if len(languages) > 0:
                language = languages[0]
            language_other = None
            if language_includes_non_specific_category:
                language_other = l.language

            airtable_language = airtable_languages_models.CreateAirtableLanguageFields(
                socio_economic_background=[socio_economic_id],
                language_dropdown=language,
                language_other=language_other,
                is_primary_language=True,
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
        for m in self.montessori_certifications:
            certification_levels, _ = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.montessori_certification_levels, m.certification_levels
            )

            (
                certifiers,
                certifier_includes_non_specific_category,
            ) = airtable_client.map_response_to_field_category_values(
                FieldCategoryType.montessori_certifiers, m.certifier
            )
            certifier = None
            if len(certifiers) > 0:
                certifier = certifiers[0]
            certifier_other = None
            if certifier_includes_non_specific_category:
                certifier_other = m.certifier

            certification_status = None
            if m.is_montessori_certified:
                certification_status = CertificationStatus.CERTIFIED
            elif m.is_seeking_montessori_certification:
                certification_status = CertificationStatus.TRAINING

            airtable_montessori_certification = (
                airtable_montessori_certifications_models.CreateAirtableMontessoriCertificationFields(
                    educator=[educator_id],
                    year_certified=m.year_certified,
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
        for e in airtable_educators.__root__:
            educator_responses.append(
                APIEducatorData.from_airtable_educator(airtable_educator=e, url_path_for=url_path_for)
            )

        return cls(__root__=educator_responses)
