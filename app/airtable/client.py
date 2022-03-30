from cachetools import cached, TTLCache
from typing import Generator, Union

from .base_school_db.field_categories import FieldCategoryType
from .. import const
from ..utils.singleton import Singleton
from .api import Api
from . import formulas
from .base_school_db import \
    const as school_db_base, \
    contact_info as contact_info_models, \
    hubs as hub_models, \
    guides_schools as guides_schools_models, \
    pods as pod_models, \
    montessori_certifications as montessori_certifications_models, \
    languages as languages_models, \
    educators as educator_models, \
    educators_schools as educators_schools_models, \
    schools as school_models, \
    socio_economic_backgrounds as socio_economic_models, \
    partners as partner_models, \
    field_categories as field_category_models, \
    field_mapping as field_mapping_models
from .base_start_school_first_contact import \
    const as start_school_first_contact_base, \
    location_contacts as location_contacts_models
from .base_ssj_typeform_responses import const as start_a_school_base, \
    start_a_school as start_a_school_models


class AirtableClient(metaclass=Singleton):
    def __init__(self, api_key=const.AIRTABLE_API_KEY):
        self.client_api = Api(api_key)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def list_hubs(self):
        raw = self.client_api.all(base_id=school_db_base.BASE_ID, table_name=school_db_base.HUBS_TABLE_NAME)
        return hub_models.ListAirtableHubResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_hub_by_id(self, hub_id):
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.HUBS_TABLE_NAME,
            record_id=hub_id)
        return hub_models.AirtableHubResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_hub_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("School Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.HUBS_TABLE_NAME,
            formula=formula)

        raw_item = None
        if len(raw) > 0:
            raw_item = raw[0]

        return hub_models.AirtableHubResponse.parse_obj(raw_item)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_hub_by_pod_id(self, pod_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(pod_id), formulas.FIELD("Pod Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.HUBS_TABLE_NAME,
            formula=formula)

        raw_item = None
        if len(raw) > 0:
            raw_item = raw[0]

        return hub_models.AirtableHubResponse.parse_obj(raw_item)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_hubs_by_entrepreneur_id(self, partner_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Regional Entrepreneur Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.HUBS_TABLE_NAME,
            formula=formula)
        return hub_models.ListAirtableHubResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def list_pods(self):
        raw = self.client_api.all(base_id=school_db_base.BASE_ID, table_name=school_db_base.PODS_TABLE_NAME)
        return pod_models.ListAirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_pod_by_id(self, pod_id):
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PODS_TABLE_NAME,
            record_id=pod_id)
        return pod_models.AirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_pod_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("School Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PODS_TABLE_NAME,
            formula=formula)

        if len(raw) > 0:
            raw_item = raw[0]
            return pod_models.AirtablePodResponse.parse_obj(raw_item)

        return None

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_pods_by_hub_id(self, hub_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(hub_id), formulas.FIELD("Hub Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PODS_TABLE_NAME,
            formula=formula)
        return pod_models.ListAirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_pods_by_contact_id(self, partner_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Pod Contact Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PODS_TABLE_NAME,
            formula=formula)
        return pod_models.ListAirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def list_schools(self, page_size=100, offset=None):
        raw, res_offset = self.client_api.paginate(
            school_db_base.BASE_ID, table_name=school_db_base.SCHOOLS_TABLE_NAME, offset=offset, page_size=page_size)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw), res_offset

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_school_by_id(self, school_id):
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.SCHOOLS_TABLE_NAME,
            record_id=school_id)
        return school_models.AirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_schools_by_hub_id(self, hub_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(hub_id), formulas.FIELD("Hub Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.SCHOOLS_TABLE_NAME,
            formula=formula)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_schools_by_pod_id(self, pod_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(pod_id), formulas.FIELD("Pod Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.SCHOOLS_TABLE_NAME,
            formula=formula)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_schools_by_educator_id(self, educator_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(educator_id), formulas.FIELD("All Educator Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.SCHOOLS_TABLE_NAME,
            formula=formula)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_schools_by_guide_id(self, partner_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Guide Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.SCHOOLS_TABLE_NAME,
            formula=formula)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_guide_school_by_id(self, guide_school_id):
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.GUIDES_SCHOOLS_TABLE_NAME,
            record_id=guide_school_id)
        return guides_schools_models.AirtableGuidesSchoolsResponse.parse_obj(raw)

    def list_guide_schools_by_ids(self, guide_school_ids=[]):
        match_formulas = []
        for gs_id in guide_school_ids:
            match_formulas.append(formulas.EQUAL(formulas.STR_VALUE(gs_id), formulas.FIELD("Record ID")))

        formula = formulas.OR(*match_formulas)
        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.GUIDES_SCHOOLS_TABLE_NAME,
            formula=formula)
        return guides_schools_models.ListAirtableGuidesSchoolsResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def list_partners(self, page_size=100, offset=None):
        raw, res_offset = self.client_api.paginate(
            school_db_base.BASE_ID, table_name=school_db_base.PARTNERS_TABLE_NAME, offset=offset, page_size=page_size)
        return partner_models.ListAirtablePartnerResponse.parse_obj(raw), res_offset

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_partner_by_id(self, school_id):
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PARTNERS_TABLE_NAME,
            record_id=school_id)
        return partner_models.AirtablePartnerResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_partners_by_hub_id(self, hub_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(hub_id), formulas.FIELD("Hub Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PARTNERS_TABLE_NAME,
            formula=formula)
        return partner_models.ListAirtablePartnerResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_partners_by_pod_id(self, pod_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(pod_id), formulas.FIELD("Pod Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PARTNERS_TABLE_NAME,
            formula=formula)
        return partner_models.ListAirtablePartnerResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_partners_by_educator_id(self, educator_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(educator_id), formulas.FIELD("Educator Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PARTNERS_TABLE_NAME,
            formula=formula)
        return partner_models.ListAirtablePartnerResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_guides_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Guided School Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PARTNERS_TABLE_NAME,
            formula=formula)
        return partner_models.ListAirtablePartnerResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def list_educators(self, page_size=100, offset=None):
        raw, res_offset = self.client_api.paginate(
            school_db_base.BASE_ID, table_name=school_db_base.EDUCATORS_TABLE_NAME, offset=offset, page_size=page_size)
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw), res_offset

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_educator_by_id(self, educator_id):
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            record_id=educator_id)
        return educator_models.AirtableEducatorResponse.parse_obj(raw)

    def get_educators_by_email(self, educator_email):
        formula = formulas.INCLUDE(formulas.STR_VALUE(educator_email), formulas.FIELD("Contact Email"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            formula=formula)
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw)

    def create_educator(self, payload: educator_models.CreateAirtableEducatorFields):
        raw = self.client_api.create(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            fields=payload.dict(by_alias=True)
        )
        return educator_models.AirtableEducatorResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_educators_by_guide_id(self, partner_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Assigned Partner Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            formula=formula)
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_primary_contacts_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Primary Contact School Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            formula=formula)
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_all_educators_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("School Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            formula=formula)
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_current_educators_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Current Educator School Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            formula=formula)
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_current_tls_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Current TL School Records IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            formula=formula)
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_founders_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Founder School Records IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            formula=formula)
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_educator_school_by_id(self, educator_school_id):
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_SCHOOLS_TABLE_NAME,
            record_id=educator_school_id)
        return educators_schools_models.AirtableEducatorsSchoolsResponse.parse_obj(raw)

    def list_educator_schools_by_ids(self, educator_school_ids):
        match_formulas = []
        for es_id in educator_school_ids:
            match_formulas.append(formulas.EQUAL(formulas.STR_VALUE(es_id), formulas.FIELD("Record ID")))

        formula = formulas.OR(*match_formulas)
        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_SCHOOLS_TABLE_NAME,
            formula=formula)
        return educators_schools_models.ListAirtableEducatorsSchoolsResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_montessori_education_by_id(self, montessori_certification_id):
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.MONTESSORI_CERTIFICATIONS_TABLE_NAME,
            record_id=montessori_certification_id)
        return montessori_certifications_models.AirtableMontessoriCertificationResponse.parse_obj(raw)

    def create_montessori_certification(
            self, payload: montessori_certifications_models.CreateAirtableMontessoriCertificationFields):
        raw = self.client_api.create(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.MONTESSORI_CERTIFICATIONS_TABLE_NAME,
            fields=payload.dict(by_alias=True))
        return montessori_certifications_models.AirtableMontessoriCertificationResponse.parse_obj(raw)

    def list_montessori_certifications_by_ids(self, montessori_certification_ids):
        match_formulas = []
        for m_id in montessori_certification_ids:
            match_formulas.append(formulas.EQUAL(formulas.STR_VALUE(m_id), formulas.FIELD("Record ID")))

        formula = formulas.OR(*match_formulas)
        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.MONTESSORI_CERTIFICATIONS_TABLE_NAME,
            formula=formula)
        return montessori_certifications_models.ListAirtableMontessoriCertificationResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_language_by_id(self, language_id):
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.LANGUAGES_TABLE_NAME,
            record_id=language_id)
        return languages_models.AirtableLanguageResponse.parse_obj(raw)

    def create_language(self, payload: languages_models.CreateAirtableLanguageFields):
        raw = self.client_api.create(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.LANGUAGES_TABLE_NAME,
            fields=payload.dict(by_alias=True)
        )
        return languages_models.AirtableLanguageResponse.parse_obj(raw)

    def list_languages_by_ids(self, language_ids):
        match_formulas = []
        for l_id in language_ids:
            match_formulas.append(formulas.EQUAL(formulas.STR_VALUE(l_id), formulas.FIELD("Record ID")))

        formula = formulas.OR(*match_formulas)
        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.LANGUAGES_TABLE_NAME,
            formula=formula)
        return languages_models.ListAirtableLanguageResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def list_location_contacts(self):
        raw = self.client_api.all(
            base_id=start_school_first_contact_base.BASE_ID,
            table_name=start_school_first_contact_base.LOCATION_CONTACT_TABLE_NAME)
        return location_contacts_models.ListAirtableLocationContactResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=64, ttl=600))
    def get_location_contact_by_id(self, location_contact_id):
        raw = self.client_api.get(
            base_id=start_school_first_contact_base.BASE_ID,
            table_name=start_school_first_contact_base.LOCATION_CONTACT_TABLE_NAME,
            record_id=location_contact_id)
        return location_contacts_models.AirtableLocationContactResponse.parse_obj(raw)

    def create_start_a_school_response(self, payload: start_a_school_models.CreateAirtableSSJTypeformStartASchool):
        raw = self.client_api.create(
            base_id=start_a_school_base.BASE_ID,
            table_name=start_a_school_base.SSJ_TYPEFORM_RESPONSES_TABLE_NAME,
            fields=payload.dict(by_alias=True)
        )
        return start_a_school_models.AirtableSSJTypeformStartASchoolResponse.parse_obj(raw)

    def create_contact_info(self, payload: contact_info_models.CreateAirtableContactInfoFields):
        raw = self.client_api.create(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.CONTACT_INFO_TABLE_NAME,
            fields=payload.dict(by_alias=True)
        )
        return contact_info_models.AirtableContactInfoResponse.parse_obj(raw)

    def create_socio_economic(self, payload: socio_economic_models.CreateAirtableSocioEconomicBackgroundFields):
        raw = self.client_api.create(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.SOCIO_ECONOMIC_BACKGROUNDS_TABLE_NAME,
            fields=payload.dict(by_alias=True)
        )
        return socio_economic_models.AirtableSocioEconomicBackgroundResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def list_field_categories(self) -> field_category_models.ListAirtableFieldCategoriesResponse:
        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.FIELD_CATEGORIES_TABLE_NAME)
        return field_category_models.ListAirtableFieldCategoriesResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def list_field_mappings(self) -> field_mapping_models.ListAirtableFieldMappingResponse:
        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.FIELD_MAPPING_TABLE_NAME)
        return field_mapping_models.ListAirtableFieldMappingResponse.parse_obj(raw)

    def map_response_to_field_category_values(self, field_category_type: FieldCategoryType, response_value: Union[str, list[str]]) -> (list[str], bool):
        field_categories = self.list_field_categories()
        field_mappings = self.list_field_mappings()

        if isinstance(response_value, list):
            all_categories = []
            includes_non_specific_category = False
            for v in response_value:
                categories, _includes_non_specific_category = self.map_response_to_field_category_values(field_category_type, v)
                if includes_non_specific_category is False and _includes_non_specific_category is True:
                    includes_non_specific_category = True

                all_categories.extend(categories)

            # Return a unique list of category values and a boolean denoting whether any category is a 'non_specific_category' type
            return list(set(all_categories)), includes_non_specific_category

        mapping = field_mappings.map_response_value(field_category_type, response_value)
        if mapping is None:
            # If response_value isn't found, try to return the 'Other' option for the given field_category_type
            mapping = field_mappings.map_response_value(field_category_type, 'Other')
        if mapping is None:
            # If response_value is still None, return empty category list and a True flag denoting the 'otherness' of the given response_value
            return [], True

        # Convert the mapping record to it's associated categories
        category_matches = field_categories.get_records_for_field_category_ids(mapping.fields.field_categories)
        # Check if any of the matching categories are a 'non_specific_category' type
        includes_non_specific_category = len(list(filter(lambda c: c.fields.non_specific_category, category_matches.__root__))) > 0
        return list(map(lambda c: c.fields.value, category_matches.__root__)), includes_non_specific_category


def get_airtable_client_generator() -> Generator:
    client = AirtableClient()
    yield client
