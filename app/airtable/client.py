from cachetools import cached, TTLCache
from typing import Generator

from ..utils.singleton import Singleton
from .api import Api
from . import formulas
from .base_school_db import *
from .base_map_by_geographic_area import (
    const as map_by_geographic_area_base,
    geo_area_contacts as geo_area_contacts_models,
    geo_area_target_communities as geo_area_target_communities_models,
)


class AirtableClient(metaclass=Singleton):
    def __init__(self, api_key=const.AIRTABLE_API_KEY):
        self.client_api = Api(api_key)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def list_hubs(self) -> ListAirtableHubResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=HUBS_TABLE_NAME).all()
        return ListAirtableHubResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_hub_by_id(self, hub_id) -> AirtableHubResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=HUBS_TABLE_NAME).get(record_id=hub_id)
        return AirtableHubResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_hub_by_school_id(self, school_id) -> Optional[AirtableHubResponse]:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("School Record IDs"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=HUBS_TABLE_NAME).all(formula=formula)

        if len(raw) > 0:
            raw_item = raw[0]
        else:
            return None

        return AirtableHubResponse.parse_obj(raw_item)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_hub_by_pod_id(self, pod_id) -> Optional[AirtableHubResponse]:
        formula = formulas.INCLUDE(formulas.STR_VALUE(pod_id), formulas.FIELD("Pod Record IDs"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=HUBS_TABLE_NAME).all(formula=formula)

        if len(raw) > 0:
            raw_item = raw[0]
        else:
            return None

        return AirtableHubResponse.parse_obj(raw_item)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_hubs_by_entrepreneur_id(self, partner_id) -> ListAirtableHubResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Regional Entrepreneur Record ID"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=HUBS_TABLE_NAME).all(formula=formula)
        return ListAirtableHubResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def list_pods(self) -> ListAirtablePodResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=PODS_TABLE_NAME).all()
        return ListAirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_pod_by_id(self, pod_id) -> AirtablePodResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=PODS_TABLE_NAME).get(record_id=pod_id)
        return AirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_pod_by_school_id(self, school_id) -> Optional[AirtablePodResponse]:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("School Record IDs"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=PODS_TABLE_NAME).all(formula=formula)

        if len(raw) > 0:
            raw_item = raw[0]
            return AirtablePodResponse.parse_obj(raw_item)

        return None

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_pods_by_hub_id(self, hub_id) -> ListAirtablePodResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(hub_id), formulas.FIELD("Hub Record ID"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=PODS_TABLE_NAME).all(formula=formula)
        return ListAirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_pods_by_contact_id(self, partner_id) -> ListAirtablePodResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Pod Contact Record ID"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=PODS_TABLE_NAME).all(formula=formula)
        return ListAirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def list_schools(self, page_size=100, offset=None) -> (ListAirtableSchoolResponse, str):
        raw, res_offset = self.client_api.paginate(
            BASE_ID, table_name=SCHOOLS_TABLE_NAME, offset=offset, page_size=page_size
        )
        return ListAirtableSchoolResponse.parse_obj(raw), res_offset

    def find_schools(self, filters: dict) -> ListAirtableSchoolResponse:
        match_formulas = []
        for field, value in filters.items():
            match_formulas.append(formulas.INCLUDE(formulas.STR_VALUE(value), formulas.FIELD(field)))

        formula = formulas.AND(*match_formulas)
        raw = self.client_api.table(base_id=BASE_ID, table_name=SCHOOLS_TABLE_NAME).all(formula=formula)

        if len(raw) == 0:
            return ListAirtableSchoolResponse()

        return ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_school_by_id(self, school_id) -> AirtableSchoolResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=SCHOOLS_TABLE_NAME).get(record_id=school_id)
        return AirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_schools_by_hub_id(self, hub_id) -> ListAirtableSchoolResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(hub_id), formulas.FIELD("Hub Record ID"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=SCHOOLS_TABLE_NAME).all(formula=formula)
        return ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_schools_by_pod_id(self, pod_id) -> ListAirtableSchoolResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(pod_id), formulas.FIELD("Pod Record ID"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=SCHOOLS_TABLE_NAME).all(formula=formula)
        return ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_schools_by_educator_id(self, educator_id) -> ListAirtableSchoolResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(educator_id), formulas.FIELD("All Educator Record IDs"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=SCHOOLS_TABLE_NAME).all(formula=formula)
        return ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_schools_by_guide_id(self, partner_id) -> ListAirtableSchoolResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Guide Record IDs"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=SCHOOLS_TABLE_NAME).all(formula=formula)
        return ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_guide_school_by_id(self, guide_school_id) -> AirtableGuidesSchoolsResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=GUIDES_SCHOOLS_TABLE_NAME).get(
            record_id=guide_school_id
        )
        return AirtableGuidesSchoolsResponse.parse_obj(raw)

    def list_guide_schools_by_ids(self, guide_school_ids=None) -> ListAirtableGuidesSchoolsResponse:
        if guide_school_ids is None:
            guide_school_ids = []

        match_formulas = []
        for gs_id in guide_school_ids:
            match_formulas.append(formulas.EQUAL(formulas.STR_VALUE(gs_id), formulas.FIELD("Record ID")))

        formula = formulas.OR(*match_formulas)
        raw = self.client_api.table(base_id=BASE_ID, table_name=GUIDES_SCHOOLS_TABLE_NAME).all(formula=formula)
        return ListAirtableGuidesSchoolsResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def list_partners(self, page_size=100, offset=None, load_relationships=True) -> (ListAirtablePartnerResponse, str):
        raw, res_offset = self.client_api.paginate(
            BASE_ID, table_name=PARTNERS_TABLE_NAME, offset=offset, page_size=page_size
        )

        response = ListAirtablePartnerResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response, res_offset

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_partner_by_id(self, school_id, load_relationships=True) -> AirtablePartnerResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=PARTNERS_TABLE_NAME).get(record_id=school_id)
        response = AirtablePartnerResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_partner_by_synced_record_id(self, synced_record_id, load_relationships=True) -> AirtablePartnerResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(synced_record_id), formulas.FIELD("Synced Record ID"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=PARTNERS_TABLE_NAME).first(formula=formula)
        response = AirtablePartnerResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

            return response

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_partners_by_hub_id(self, hub_id, load_relationships=True) -> ListAirtablePartnerResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(hub_id), formulas.FIELD("Hub Record ID"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=PARTNERS_TABLE_NAME).all(formula=formula)
        response = ListAirtablePartnerResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_partners_by_pod_id(self, pod_id, load_relationships=True) -> ListAirtablePartnerResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(pod_id), formulas.FIELD("Pod Record ID"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=PARTNERS_TABLE_NAME).all(formula=formula)
        response = ListAirtablePartnerResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_partners_by_educator_id(self, educator_id, load_relationships=True) -> ListAirtablePartnerResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(educator_id), formulas.FIELD("Educator Record IDs"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=PARTNERS_TABLE_NAME).all(formula=formula)
        response = ListAirtablePartnerResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_guides_by_school_id(self, school_id, load_relationships=True) -> ListAirtablePartnerResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Guided School Record ID"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=PARTNERS_TABLE_NAME).all(formula=formula)
        response = ListAirtablePartnerResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def list_educators(
        self, page_size=100, offset=None, load_relationships=True
    ) -> (ListAirtableEducatorResponse, str):
        raw, res_offset = self.client_api.paginate(
            BASE_ID, table_name=EDUCATORS_TABLE_NAME, offset=offset, page_size=page_size
        )
        response = ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response, res_offset

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_educator_by_id(self, educator_id, load_relationships=True) -> AirtableEducatorResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_TABLE_NAME).get(record_id=educator_id)
        response = AirtableEducatorResponse.parse_obj(raw)
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
        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_TABLE_NAME).all(formula=formula)

        if len(raw) == 0:
            return ListAirtableEducatorResponse(__root__=[])

        response = ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    def create_educator(
        self, payload: CreateAirtableEducatorFields, load_relationships=True
    ) -> AirtableEducatorResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_TABLE_NAME).create(
            fields=payload.dict(by_alias=True)
        )
        response = AirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    def add_typeform_start_a_school_response_to_educator(
        self, educator_id, typeform_start_a_school_response_id, load_relationships=True
    ) -> AirtableEducatorResponse:
        educator = self.get_educator_by_id(educator_id)
        start_school_typeforms = educator.fields.ssj_typeforms_start_a_school

        if typeform_start_a_school_response_id in start_school_typeforms:
            return educator

        start_school_typeforms.append(typeform_start_a_school_response_id)

        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_TABLE_NAME).update(
            record_id=educator_id,
            fields={AirtableEducatorFields.__fields__["ssj_typeforms_start_a_school"].alias: start_school_typeforms},
        )
        response = AirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_educators_by_guide_id(self, partner_id, load_relationships=True) -> ListAirtableEducatorResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Assigned Partner Record ID"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_TABLE_NAME).all(formula=formula)

        response = ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_primary_contacts_by_school_id(self, school_id, load_relationships=True) -> ListAirtableEducatorResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Primary Contact School Record IDs"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_TABLE_NAME).all(formula=formula)
        response = ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_all_educators_by_school_id(self, school_id, load_relationships=True) -> ListAirtableEducatorResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("School Record IDs"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_TABLE_NAME).all(formula=formula)
        response = ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_current_educators_by_school_id(self, school_id, load_relationships=True) -> ListAirtableEducatorResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Current Educator School Record IDs"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_TABLE_NAME).all(formula=formula)
        response = ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_current_tls_by_school_id(self, school_id, load_relationships=True) -> ListAirtableEducatorResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Current TL School Records IDs"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_TABLE_NAME).all(formula=formula)
        response = ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_founders_by_school_id(self, school_id, load_relationships=True) -> ListAirtableEducatorResponse:
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Founder School Records IDs"))

        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_TABLE_NAME).all(formula=formula)
        response = ListAirtableEducatorResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()

        return response

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_educator_school_by_id(
        self, educator_school_id, load_relationships=True
    ) -> AirtableEducatorsSchoolsResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_SCHOOLS_TABLE_NAME).get(
            record_id=educator_school_id
        )
        response = AirtableEducatorsSchoolsResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()
        return response

    def create_educator_schools(
        self, payload: CreateUpdateAirtableEducatorsSchoolsFields
    ) -> AirtableEducatorsSchoolsResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_SCHOOLS_TABLE_NAME).create(
            fields=payload.dict(by_alias=True)
        )
        return AirtableEducatorsSchoolsResponse.parse_obj(raw)

    def update_educator_schools(
        self, record_id: str, payload: CreateUpdateAirtableEducatorsSchoolsFields
    ) -> AirtableEducatorsSchoolsResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_SCHOOLS_TABLE_NAME).update(
            record_id=record_id,
            fields=payload.dict(by_alias=True),
        )
        return AirtableEducatorsSchoolsResponse.parse_obj(raw)

    def list_educator_schools_by_ids(
        self, educator_school_ids, load_relationships=True
    ) -> ListAirtableEducatorsSchoolsResponse:
        match_formulas = []
        for es_id in educator_school_ids:
            match_formulas.append(formulas.EQUAL(formulas.STR_VALUE(es_id), formulas.FIELD("Record ID")))

        formula = formulas.OR(*match_formulas)
        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_SCHOOLS_TABLE_NAME).all(formula=formula)
        response = ListAirtableEducatorsSchoolsResponse.parse_obj(raw)
        if load_relationships:
            response.load_relationships()
        return response

    def find_educator_schools(self, filters: dict) -> ListAirtableEducatorsSchoolsResponse:
        match_formulas = []
        for field, value in filters.items():
            match_formulas.append(formulas.INCLUDE(formulas.STR_VALUE(value), formulas.FIELD(field)))

        formula = formulas.AND(*match_formulas)
        # formula = match_formulas[0]
        raw = self.client_api.table(base_id=BASE_ID, table_name=EDUCATORS_SCHOOLS_TABLE_NAME).all(formula=formula)

        if len(raw) == 0:
            return ListAirtableEducatorsSchoolsResponse(__root__=[])

        return ListAirtableEducatorsSchoolsResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_montessori_education_by_id(self, montessori_certification_id) -> AirtableMontessoriCertificationResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=MONTESSORI_CERTIFICATIONS_TABLE_NAME).get(
            record_id=montessori_certification_id
        )
        return AirtableMontessoriCertificationResponse.parse_obj(raw)

    def create_montessori_certification(
        self, payload: CreateAirtableMontessoriCertificationFields
    ) -> AirtableMontessoriCertificationResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=MONTESSORI_CERTIFICATIONS_TABLE_NAME).create(
            fields=payload.dict(by_alias=True)
        )
        return AirtableMontessoriCertificationResponse.parse_obj(raw)

    def list_montessori_certifications_by_ids(
        self, montessori_certification_ids
    ) -> ListAirtableMontessoriCertificationResponse:
        match_formulas = []
        for m_id in montessori_certification_ids:
            match_formulas.append(formulas.EQUAL(formulas.STR_VALUE(m_id), formulas.FIELD("Record ID")))

        formula = formulas.OR(*match_formulas)
        raw = self.client_api.table(base_id=BASE_ID, table_name=MONTESSORI_CERTIFICATIONS_TABLE_NAME).all(
            formula=formula
        )
        return ListAirtableMontessoriCertificationResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_language_by_id(self, language_id) -> AirtableLanguageResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=LANGUAGES_TABLE_NAME).get(record_id=language_id)
        return AirtableLanguageResponse.parse_obj(raw)

    def create_language(self, payload: CreateAirtableLanguageFields) -> AirtableLanguageResponse:
        raw = (self.client_api.table(base_id=BASE_ID, table_name=LANGUAGES_TABLE_NAME)).create(
            fields=payload.dict(by_alias=True)
        )
        return AirtableLanguageResponse.parse_obj(raw)

    def list_languages_by_ids(self, language_ids) -> ListAirtableLanguageResponse:
        match_formulas = []
        for l_id in language_ids:
            match_formulas.append(formulas.EQUAL(formulas.STR_VALUE(l_id), formulas.FIELD("Record ID")))

        formula = formulas.OR(*match_formulas)
        raw = self.client_api.table(base_id=BASE_ID, table_name=LANGUAGES_TABLE_NAME).all(formula=formula)
        return ListAirtableLanguageResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def list_geo_area_contacts(self) -> geo_area_contacts_models.ListAirtableGeoAreaContactResponse:
        raw = self.client_api.table(
            base_id=map_by_geographic_area_base.BASE_ID, table_name=map_by_geographic_area_base.AREA_CONTACT_TABLE_NAME
        ).all()
        return geo_area_contacts_models.ListAirtableGeoAreaContactResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=64, ttl=600))
    def get_geo_area_contact_by_id(
        self, geo_area_contact_id
    ) -> geo_area_contacts_models.AirtableGeoAreaContactResponse:
        raw = self.client_api.table(
            base_id=map_by_geographic_area_base.BASE_ID,
            table_name=map_by_geographic_area_base.AREA_CONTACT_TABLE_NAME,
        ).get(record_id=geo_area_contact_id)
        return geo_area_contacts_models.AirtableGeoAreaContactResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def list_geo_area_target_communities(
        self,
    ) -> geo_area_target_communities_models.ListAirtableGeoAreaTargetCommunityResponse:
        raw = self.client_api.table(
            base_id=map_by_geographic_area_base.BASE_ID,
            table_name=map_by_geographic_area_base.AREA_TARGET_COMMUNITY_TABLE_NAME,
        ).all()
        return geo_area_target_communities_models.ListAirtableGeoAreaTargetCommunityResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=64, ttl=600))
    def get_geo_area_target_community_by_id(
        self, geo_area_target_community_id
    ) -> geo_area_target_communities_models.AirtableGeoAreaTargetCommunityResponse:
        raw = self.client_api.table(
            base_id=map_by_geographic_area_base.BASE_ID,
            table_name=map_by_geographic_area_base.AREA_TARGET_COMMUNITY_TABLE_NAME,
        ).get(
            record_id=geo_area_target_community_id,
        )
        return geo_area_target_communities_models.AirtableGeoAreaTargetCommunityResponse.parse_obj(raw)

    def create_start_a_school_response(
        self, payload: CreateAirtableSSJTypeformStartASchool
    ) -> AirtableSSJTypeformStartASchoolResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=SSJ_TYPEFORM_RESPONSES_TABLE_NAME).create(
            fields=payload.dict(by_alias=True)
        )
        return AirtableSSJTypeformStartASchoolResponse.parse_obj(raw)

    # 7/15/2022 - Moved away from Contact Info for a more flat structure in the Educator table itself
    # def create_contact_info(self, payload: CreateAirtableContactInfoFields) -> AirtableContactInfoResponse:
    #     raw = self.client_api.table(
    #         base_id=BASE_ID, table_name=CONTACT_INFO_TABLE_NAME
    #     ).create(
    #         fields=payload.dict(by_alias=True)
    #     )
    #     return AirtableContactInfoResponse.parse_obj(raw)

    def create_socio_economic(
        self, payload: CreateAirtableSocioEconomicBackgroundFields
    ) -> AirtableSocioEconomicBackgroundResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=SOCIO_ECONOMIC_BACKGROUNDS_TABLE_NAME).create(
            fields=payload.dict(by_alias=True)
        )
        return AirtableSocioEconomicBackgroundResponse.parse_obj(raw)

    def list_newsletters_by_ids(self, newsletter_ids) -> ListAirtableNewsletterResponse:
        match_formulas = []
        for n_id in newsletter_ids:
            match_formulas.append(formulas.EQUAL(formulas.STR_VALUE(n_id), formulas.FIELD("Record ID")))

        formula = formulas.OR(*match_formulas)
        raw = self.client_api.table(base_id=BASE_ID, table_name=NEWSLETTERS_TABLE_NAME).all(formula=formula)
        return ListAirtableNewsletterResponse.parse_obj(raw)

    def get_newsletters_by_slug(self, slugs: list[NewsletterSlugs]) -> ListAirtableNewsletterResponse:
        match_formulas = []
        for s in slugs:
            match_formulas.append(formulas.EQUAL(formulas.STR_VALUE(s.value), formulas.FIELD("Slug")))

        formula = formulas.OR(*match_formulas)
        raw = self.client_api.table(base_id=BASE_ID, table_name=NEWSLETTERS_TABLE_NAME).all(formula=formula)
        return ListAirtableNewsletterResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def list_field_categories(self) -> ListAirtableFieldCategoriesResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=FIELD_CATEGORIES_TABLE_NAME)
        return ListAirtableFieldCategoriesResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def list_field_mappings(self) -> ListAirtableFieldMappingResponse:
        raw = self.client_api.table(base_id=BASE_ID, table_name=FIELD_MAPPING_TABLE_NAME)
        return ListAirtableFieldMappingResponse.parse_obj(raw)

    def map_response_to_field_category_values(
        self, field_category_type: FieldCategoryType, response_value: Union[str, list[str]]
    ) -> (list[str], bool):
        if response_value is None:
            return [], False

        field_categories = self.list_field_categories()
        field_mappings = self.list_field_mappings()

        if isinstance(response_value, list):
            all_categories = []
            includes_non_specific_category = False
            for v in response_value:
                categories, _includes_non_specific_category = self.map_response_to_field_category_values(
                    field_category_type, v
                )
                if includes_non_specific_category is False and _includes_non_specific_category is True:
                    includes_non_specific_category = True

                all_categories.extend(categories)

            # Return a unique list of category values and a boolean denoting whether
            # any category is a 'non_specific_category' type
            return list(set(all_categories)), includes_non_specific_category

        mapping = field_mappings.map_response_value(field_category_type, response_value)
        if mapping is None:
            # If response_value isn't found, try to return the 'Other' option for the given field_category_type
            mapping = field_mappings.map_response_value(field_category_type, "Other")
        if mapping is None:
            # If response_value is still None, return empty category list and a True
            # flag denoting the 'otherness' of the given response_value
            return [], True

        # Convert the mapping record to it's associated categories
        category_matches = field_categories.get_records_for_field_category_ids(mapping.fields.field_categories)
        # Check if any of the matching categories are a 'non_specific_category' type
        includes_non_specific_category = (
            len(list(filter(lambda c: c.fields.non_specific_category, category_matches.__root__))) > 0
        )
        return list(map(lambda c: c.fields.value, category_matches.__root__)), includes_non_specific_category


def get_airtable_client_generator() -> Generator:
    client = AirtableClient()
    yield client
