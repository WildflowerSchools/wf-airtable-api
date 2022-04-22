from cachetools import cached, TTLCache
from typing import Generator, Union, Optional, List, Any

from .base_school_db.educators import ListAirtableEducatorResponse
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
    newsletters as newsletters_models, \
    languages as languages_models, \
    educators as educator_models, \
    educators_schools as educators_schools_models, \
    schools as school_models, \
    socio_economic_backgrounds as socio_economic_models, \
    partners as partner_models, \
    field_categories as field_category_models, \
    field_mapping as field_mapping_models, \
    typeform_start_a_school as typeform_start_a_school_models
from .base_map_by_geographic_area import \
    const as map_by_geographic_area_base, \
    geo_area_contacts as geo_area_contacts_models, \
    geo_area_target_communities as geo_area_target_communities_models


class AirtableClient(metaclass=Singleton):
    def __init__(self, api_key=const.AIRTABLE_API_KEY):
        self.client_api = Api(api_key)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def list_hubs(self) -> hub_models.ListAirtableHubResponse:
        raw = self.client_api.all(base_id=school_db_base.BASE_ID, table_name=school_db_base.HUBS_TABLE_NAME)
        return hub_models.ListAirtableHubResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_hub_by_id(self, hub_id) -> hub_models.AirtableHubResponse:
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.HUBS_TABLE_NAME,
            record_id=hub_id)
        return hub_models.AirtableHubResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_hub_by_school_id(self, school_id) -> Optional[hub_models.AirtableHubResponse]:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("School Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.HUBS_TABLE_NAME,
            formula=formula)

        if len(raw) > 0:
            raw_item = raw[0]
        else:
            return None

        return hub_models.AirtableHubResponse.parse_obj(raw_item)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_hub_by_pod_id(self, pod_id) -> Optional[hub_models.AirtableHubResponse]:
        formula = formulas.INCLUDE(formulas.STR_VALUE(pod_id), formulas.FIELD("Pod Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.HUBS_TABLE_NAME,
            formula=formula)

        if len(raw) > 0:
            raw_item = raw[0]
        else:
            return None

        return hub_models.AirtableHubResponse.parse_obj(raw_item)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_hubs_by_entrepreneur_id(self, partner_id) -> hub_models.ListAirtableHubResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Regional Entrepreneur Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.HUBS_TABLE_NAME,
            formula=formula)
        return hub_models.ListAirtableHubResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def list_pods(self) -> pod_models.ListAirtablePodResponse:
        raw = self.client_api.all(base_id=school_db_base.BASE_ID, table_name=school_db_base.PODS_TABLE_NAME)
        return pod_models.ListAirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_pod_by_id(self, pod_id) -> pod_models.AirtablePodResponse:
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PODS_TABLE_NAME,
            record_id=pod_id)
        return pod_models.AirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_pod_by_school_id(self, school_id) -> Optional[pod_models.AirtablePodResponse]:
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
    def get_pods_by_hub_id(self, hub_id) -> pod_models.ListAirtablePodResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(hub_id), formulas.FIELD("Hub Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PODS_TABLE_NAME,
            formula=formula)
        return pod_models.ListAirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_pods_by_contact_id(self, partner_id) -> pod_models.ListAirtablePodResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Pod Contact Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PODS_TABLE_NAME,
            formula=formula)
        return pod_models.ListAirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def list_schools(self, page_size=100, offset=None) -> (school_models.ListAirtableSchoolResponse, str):
        raw, res_offset = self.client_api.paginate(
            school_db_base.BASE_ID, table_name=school_db_base.SCHOOLS_TABLE_NAME, offset=offset, page_size=page_size)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw), res_offset

    def find_schools(self, filters: dict) -> school_models.ListAirtableSchoolResponse:
        match_formulas = []
        for field, value in filters.items():
            match_formulas.append(formulas.INCLUDE(formulas.STR_VALUE(value), formulas.FIELD(field)))

        formula = formulas.AND(*match_formulas)
        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.SCHOOLS_TABLE_NAME,
            formula=formula)

        if len(raw) == 0:
            return school_models.ListAirtableSchoolResponse()

        return school_models.ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_school_by_id(self, school_id) -> school_models.AirtableSchoolResponse:
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.SCHOOLS_TABLE_NAME,
            record_id=school_id)
        return school_models.AirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_schools_by_hub_id(self, hub_id) -> school_models.ListAirtableSchoolResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(hub_id), formulas.FIELD("Hub Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.SCHOOLS_TABLE_NAME,
            formula=formula)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_schools_by_pod_id(self, pod_id) -> school_models.ListAirtableSchoolResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(pod_id), formulas.FIELD("Pod Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.SCHOOLS_TABLE_NAME,
            formula=formula)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_schools_by_educator_id(self, educator_id) -> school_models.ListAirtableSchoolResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(educator_id), formulas.FIELD("All Educator Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.SCHOOLS_TABLE_NAME,
            formula=formula)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_schools_by_guide_id(self, partner_id) -> school_models.ListAirtableSchoolResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Guide Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.SCHOOLS_TABLE_NAME,
            formula=formula)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_guide_school_by_id(self, guide_school_id) -> guides_schools_models.AirtableGuidesSchoolsResponse:
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.GUIDES_SCHOOLS_TABLE_NAME,
            record_id=guide_school_id)
        return guides_schools_models.AirtableGuidesSchoolsResponse.parse_obj(raw)

    def list_guide_schools_by_ids(
            self, guide_school_ids=None) -> guides_schools_models.ListAirtableGuidesSchoolsResponse:
        if guide_school_ids is None:
            guide_school_ids = []

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
    def list_partners(self, page_size=100, offset=None,
                      load_relationships=True) -> (partner_models.ListAirtablePartnerResponse, str):
        raw, res_offset = self.client_api.paginate(
            school_db_base.BASE_ID, table_name=school_db_base.PARTNERS_TABLE_NAME, offset=offset, page_size=page_size)

        response = partner_models.ListAirtablePartnerResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response, res_offset

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_partner_by_id(self, school_id, load_relationships=True) -> partner_models.AirtablePartnerResponse:
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PARTNERS_TABLE_NAME,
            record_id=school_id)
        response = partner_models.AirtablePartnerResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_partner_by_synced_record_id(self, synced_record_id,
                                        load_relationships=True) -> partner_models.AirtablePartnerResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(synced_record_id), formulas.FIELD("Synced Record ID"))

        raw = self.client_api.first(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PARTNERS_TABLE_NAME,
            formula=formula)
        response = partner_models.AirtablePartnerResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

            return response

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_partners_by_hub_id(self, hub_id, load_relationships=True) -> partner_models.ListAirtablePartnerResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(hub_id), formulas.FIELD("Hub Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PARTNERS_TABLE_NAME,
            formula=formula)
        response = partner_models.ListAirtablePartnerResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_partners_by_pod_id(self, pod_id, load_relationships=True) -> partner_models.ListAirtablePartnerResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(pod_id), formulas.FIELD("Pod Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PARTNERS_TABLE_NAME,
            formula=formula)
        response = partner_models.ListAirtablePartnerResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_partners_by_educator_id(
            self, educator_id, load_relationships=True) -> partner_models.ListAirtablePartnerResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(educator_id), formulas.FIELD("Educator Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PARTNERS_TABLE_NAME,
            formula=formula)
        response = partner_models.ListAirtablePartnerResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_guides_by_school_id(self, school_id, load_relationships=True) -> partner_models.ListAirtablePartnerResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Guided School Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.PARTNERS_TABLE_NAME,
            formula=formula)
        response = partner_models.ListAirtablePartnerResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def list_educators(self, page_size=100, offset=None,
                       load_relationships=True) -> (educator_models.ListAirtableEducatorResponse, str):
        raw, res_offset = self.client_api.paginate(
            school_db_base.BASE_ID, table_name=school_db_base.EDUCATORS_TABLE_NAME, offset=offset, page_size=page_size)
        response = educator_models.ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response, res_offset

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_educator_by_id(self, educator_id, load_relationships=True) -> educator_models.AirtableEducatorResponse:
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            record_id=educator_id)
        response = educator_models.AirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    def find_educators(self, filters: dict, load_relationships=True) -> ListAirtableEducatorResponse:
        match_formulas = []
        for field, value in filters.items():
            if isinstance(value, list):
                sub_match_formulas = []
                for v in value:
                    sub_match_formulas.append(formulas.INCLUDE(formulas.STR_VALUE(v), formulas.FIELD(field)))

                match_formulas.append(formulas.OR(*sub_match_formulas))
            else:
                match_formulas.append(formulas.INCLUDE(formulas.STR_VALUE(value), formulas.FIELD(field)))

        formula = formulas.AND(*match_formulas)
        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            formula=formula)

        if len(raw) == 0:
            return educator_models.ListAirtableEducatorResponse()

        response = educator_models.ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    def create_educator(
            self, payload: educator_models.CreateAirtableEducatorFields, load_relationships=True) -> educator_models.AirtableEducatorResponse:
        raw = self.client_api.create(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            fields=payload.dict(by_alias=True)
        )
        response = educator_models.AirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    def add_typeform_start_a_school_response_to_educator(
            self, educator_id, typeform_start_a_school_response_id, load_relationships=True) -> educator_models.AirtableEducatorResponse:
        educator = self.get_educator_by_id(educator_id)
        start_school_typeforms = educator.fields.ssj_typeforms_start_a_school

        if typeform_start_a_school_response_id in start_school_typeforms:
            return educator

        start_school_typeforms.append(typeform_start_a_school_response_id)

        raw = self.client_api.update(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            record_id=educator_id,
            fields={educator_models.AirtableEducatorFields.__fields__[
                'ssj_typeforms_start_a_school'].alias: start_school_typeforms}
        )
        response = educator_models.AirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_educators_by_guide_id(
            self, partner_id, load_relationships=True) -> educator_models.ListAirtableEducatorResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Assigned Partner Record ID"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            formula=formula)

        response = educator_models.ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_primary_contacts_by_school_id(
            self, school_id, load_relationships=True) -> educator_models.ListAirtableEducatorResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Primary Contact School Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            formula=formula)
        response = educator_models.ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_all_educators_by_school_id(
            self, school_id, load_relationships=True) -> educator_models.ListAirtableEducatorResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("School Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            formula=formula)
        response = educator_models.ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_current_educators_by_school_id(
            self, school_id, load_relationships=True) -> educator_models.ListAirtableEducatorResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Current Educator School Record IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            formula=formula)
        response = educator_models.ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_current_tls_by_school_id(
            self, school_id, load_relationships=True) -> educator_models.ListAirtableEducatorResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Current TL School Records IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            formula=formula)
        response = educator_models.ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_founders_by_school_id(
            self, school_id, load_relationships=True) -> educator_models.ListAirtableEducatorResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Founder School Records IDs"))

        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_TABLE_NAME,
            formula=formula)
        response = educator_models.ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_educator_school_by_id(
            self, educator_school_id,
            load_relationships=True) -> educators_schools_models.AirtableEducatorsSchoolsResponse:
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_SCHOOLS_TABLE_NAME,
            record_id=educator_school_id)
        response = educators_schools_models.AirtableEducatorsSchoolsResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()
        return response

    def list_educator_schools_by_ids(
            self, educator_school_ids,
            load_relationships=True) -> educators_schools_models.ListAirtableEducatorsSchoolsResponse:
        match_formulas = []
        for es_id in educator_school_ids:
            match_formulas.append(formulas.EQUAL(formulas.STR_VALUE(es_id), formulas.FIELD("Record ID")))

        formula = formulas.OR(*match_formulas)
        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.EDUCATORS_SCHOOLS_TABLE_NAME,
            formula=formula)
        response = educators_schools_models.ListAirtableEducatorsSchoolsResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()
        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_montessori_education_by_id(
            self, montessori_certification_id) -> montessori_certifications_models.AirtableMontessoriCertificationResponse:
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.MONTESSORI_CERTIFICATIONS_TABLE_NAME,
            record_id=montessori_certification_id)
        return montessori_certifications_models.AirtableMontessoriCertificationResponse.parse_obj(raw)

    def create_montessori_certification(
            self, payload: montessori_certifications_models.CreateAirtableMontessoriCertificationFields) -> montessori_certifications_models.AirtableMontessoriCertificationResponse:
        raw = self.client_api.create(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.MONTESSORI_CERTIFICATIONS_TABLE_NAME,
            fields=payload.dict(by_alias=True))
        return montessori_certifications_models.AirtableMontessoriCertificationResponse.parse_obj(raw)

    def list_montessori_certifications_by_ids(
            self, montessori_certification_ids) -> montessori_certifications_models.ListAirtableMontessoriCertificationResponse:
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
    def get_language_by_id(self, language_id) -> languages_models.AirtableLanguageResponse:
        raw = self.client_api.get(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.LANGUAGES_TABLE_NAME,
            record_id=language_id)
        return languages_models.AirtableLanguageResponse.parse_obj(raw)

    def create_language(
            self, payload: languages_models.CreateAirtableLanguageFields) -> languages_models.AirtableLanguageResponse:
        raw = self.client_api.create(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.LANGUAGES_TABLE_NAME,
            fields=payload.dict(by_alias=True)
        )
        return languages_models.AirtableLanguageResponse.parse_obj(raw)

    def list_languages_by_ids(self, language_ids) -> languages_models.ListAirtableLanguageResponse:
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
    def list_geo_area_contacts(self) -> geo_area_contacts_models.ListAirtableGeoAreaContactResponse:
        raw = self.client_api.all(
            base_id=map_by_geographic_area_base.BASE_ID,
            table_name=map_by_geographic_area_base.AREA_CONTACT_TABLE_NAME)
        return geo_area_contacts_models.ListAirtableGeoAreaContactResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=64, ttl=600))
    def get_geo_area_contact_by_id(
            self, geo_area_contact_id) -> geo_area_contacts_models.AirtableGeoAreaContactResponse:
        raw = self.client_api.get(
            base_id=map_by_geographic_area_base.BASE_ID,
            table_name=map_by_geographic_area_base.AREA_CONTACT_TABLE_NAME,
            record_id=geo_area_contact_id)
        return geo_area_contacts_models.AirtableGeoAreaContactResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def list_geo_area_target_communities(
            self) -> geo_area_target_communities_models.ListAirtableGeoAreaTargetCommunityResponse:
        raw = self.client_api.all(
            base_id=map_by_geographic_area_base.BASE_ID,
            table_name=map_by_geographic_area_base.AREA_TARGET_COMMUNITY_TABLE_NAME)
        return geo_area_target_communities_models.ListAirtableGeoAreaTargetCommunityResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=64, ttl=600))
    def get_geo_area_target_community_by_id(
            self, geo_area_target_community_id) -> geo_area_target_communities_models.AirtableGeoAreaTargetCommunityResponse:
        raw = self.client_api.get(
            base_id=map_by_geographic_area_base.BASE_ID,
            table_name=map_by_geographic_area_base.AREA_TARGET_COMMUNITY_TABLE_NAME,
            record_id=geo_area_target_community_id)
        return geo_area_target_communities_models.AirtableGeoAreaTargetCommunityResponse.parse_obj(raw)

    def create_start_a_school_response(
            self, payload: typeform_start_a_school_models.CreateAirtableSSJTypeformStartASchool) -> typeform_start_a_school_models.AirtableSSJTypeformStartASchoolResponse:
        raw = self.client_api.create(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.SSJ_TYPEFORM_RESPONSES_TABLE_NAME,
            fields=payload.dict(by_alias=True)
        )
        return typeform_start_a_school_models.AirtableSSJTypeformStartASchoolResponse.parse_obj(raw)

    def create_contact_info(
            self, payload: contact_info_models.CreateAirtableContactInfoFields) -> contact_info_models.AirtableContactInfoResponse:
        raw = self.client_api.create(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.CONTACT_INFO_TABLE_NAME,
            fields=payload.dict(by_alias=True)
        )
        return contact_info_models.AirtableContactInfoResponse.parse_obj(raw)

    def create_socio_economic(
            self, payload: socio_economic_models.CreateAirtableSocioEconomicBackgroundFields) -> socio_economic_models.AirtableSocioEconomicBackgroundResponse:
        raw = self.client_api.create(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.SOCIO_ECONOMIC_BACKGROUNDS_TABLE_NAME,
            fields=payload.dict(by_alias=True)
        )
        return socio_economic_models.AirtableSocioEconomicBackgroundResponse.parse_obj(raw)

    def list_newsletters_by_ids(self, newsletter_ids) -> newsletters_models.ListAirtableNewsletterResponse:
        match_formulas = []
        for n_id in newsletter_ids:
            match_formulas.append(formulas.EQUAL(formulas.STR_VALUE(n_id), formulas.FIELD("Record ID")))

        formula = formulas.OR(*match_formulas)
        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.NEWSLETTERS_TABLE_NAME,
            formula=formula)
        return newsletters_models.ListAirtableNewsletterResponse.parse_obj(raw)

    def get_newsletters_by_slug(self,
                                slugs: list[newsletters_models.NewsletterSlugs]) -> newsletters_models.ListAirtableNewsletterResponse:
        match_formulas = []
        for s in slugs:
            match_formulas.append(formulas.EQUAL(formulas.STR_VALUE(s.value), formulas.FIELD("Slug")))

        formula = formulas.OR(*match_formulas)
        raw = self.client_api.all(
            base_id=school_db_base.BASE_ID,
            table_name=school_db_base.NEWSLETTERS_TABLE_NAME,
            formula=formula)
        return newsletters_models.ListAirtableNewsletterResponse.parse_obj(raw)

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

    def map_response_to_field_category_values(
            self, field_category_type: FieldCategoryType, response_value: Union[str, list[str]]) -> (list[str], bool):
        if response_value is None:
            return [], False

        field_categories = self.list_field_categories()
        field_mappings = self.list_field_mappings()

        if isinstance(response_value, list):
            all_categories = []
            includes_non_specific_category = False
            for v in response_value:
                categories, _includes_non_specific_category = self.map_response_to_field_category_values(
                    field_category_type, v)
                if includes_non_specific_category is False and _includes_non_specific_category is True:
                    includes_non_specific_category = True

                all_categories.extend(categories)

            # Return a unique list of category values and a boolean denoting whether
            # any category is a 'non_specific_category' type
            return list(set(all_categories)), includes_non_specific_category

        mapping = field_mappings.map_response_value(field_category_type, response_value)
        if mapping is None:
            # If response_value isn't found, try to return the 'Other' option for the given field_category_type
            mapping = field_mappings.map_response_value(field_category_type, 'Other')
        if mapping is None:
            # If response_value is still None, return empty category list and a True
            # flag denoting the 'otherness' of the given response_value
            return [], True

        # Convert the mapping record to it's associated categories
        category_matches = field_categories.get_records_for_field_category_ids(mapping.fields.field_categories)
        # Check if any of the matching categories are a 'non_specific_category' type
        includes_non_specific_category = len(
            list(
                filter(
                    lambda c: c.fields.non_specific_category,
                    category_matches.__root__))) > 0
        return list(map(lambda c: c.fields.value, category_matches.__root__)), includes_non_specific_category


def get_airtable_client_generator() -> Generator:
    client = AirtableClient()
    yield client
