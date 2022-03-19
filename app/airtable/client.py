from cachetools import cached, TTLCache
from typing import Generator
from pyairtable import Api

from .. import const
from ..utils.singleton import Singleton
from . import formulas
from . import hubs as hub_models
from . import pods as pod_models
from . import schools as school_models
from . import partners as partner_models
from . import guides_schools as guides_schools_models
from . import educators_schools as educators_schools_models
from . import montessori_certifications as montessori_certifications_models
from . import languages as languages_models
from . import educators as educator_models

SCHOOLS_BASE_ID = 'appJBT9a4f3b7hWQ2'

HUBS_TABLE_NAME = 'Hubs'
PODS_TABLE_NAME = 'Pods'
SCHOOLS_TABLE_NAME = 'Schools'
EDUCATORS_TABLE_NAME = 'Educators'
PARTNERS_TABLE_NAME = 'Partners'
GUIDES_SCHOOLS_TABLE_NAME = 'Guides x Schools'
EDUCATORS_SCHOOLS_TABLE_NAME = 'Educators x Schools'
MONTESSORI_CERTIFICATIONS_TABLE_NAME = 'Montessori Certifications'
LANGUAGES_TABLE_NAME = 'Languages'


class AirtableClient(metaclass=Singleton):
    def __init__(self, api_key=const.AIRTABLE_API_KEY):
        self.client_api = Api(api_key)

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def list_hubs(self):
        raw = self.client_api.all(SCHOOLS_BASE_ID, HUBS_TABLE_NAME)
        return hub_models.ListAirtableHubResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_hub_by_id(self, hub_id):
        raw = self.client_api.get(SCHOOLS_BASE_ID, HUBS_TABLE_NAME, hub_id)
        return hub_models.AirtableHubResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_hub_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("School Record IDs"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, HUBS_TABLE_NAME, formula=formula)

        raw_item = None
        if len(raw) > 0:
            raw_item = raw[0]

        return hub_models.AirtableHubResponse.parse_obj(raw_item)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_hub_by_pod_id(self, pod_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(pod_id), formulas.FIELD("Pod Record IDs"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, HUBS_TABLE_NAME, formula=formula)

        raw_item = None
        if len(raw) > 0:
            raw_item = raw[0]

        return hub_models.AirtableHubResponse.parse_obj(raw_item)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_hubs_by_entrepreneur_id(self, partner_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Regional Entrepreneur Record ID"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, HUBS_TABLE_NAME, formula=formula)
        return hub_models.ListAirtableHubResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def list_pods(self):
        raw = self.client_api.all(SCHOOLS_BASE_ID, PODS_TABLE_NAME)
        return pod_models.ListAirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_pod_by_id(self, pod_id):
        raw = self.client_api.get(SCHOOLS_BASE_ID, PODS_TABLE_NAME, pod_id)
        return pod_models.AirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_pod_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("School Record IDs"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, PODS_TABLE_NAME, formula=formula)

        if len(raw) > 0:
            raw_item = raw[0]
            return pod_models.AirtablePodResponse.parse_obj(raw_item)

        return None

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_pods_by_hub_id(self, hub_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(hub_id), formulas.FIELD("Hub Record ID"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, PODS_TABLE_NAME, formula=formula)
        return pod_models.ListAirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_pods_by_contact_id(self, partner_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Pod Contact Record ID"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, PODS_TABLE_NAME, formula=formula)
        return pod_models.ListAirtablePodResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def list_schools(self):
        raw = self.client_api.all(SCHOOLS_BASE_ID, SCHOOLS_TABLE_NAME)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_school_by_id(self, school_id):
        raw = self.client_api.get(SCHOOLS_BASE_ID, SCHOOLS_TABLE_NAME, school_id)
        return school_models.AirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_schools_by_hub_id(self, hub_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(hub_id), formulas.FIELD("Hub Record ID"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, SCHOOLS_TABLE_NAME, formula=formula)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_schools_by_pod_id(self, pod_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(pod_id), formulas.FIELD("Pod Record ID"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, SCHOOLS_TABLE_NAME, formula=formula)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_schools_by_educator_id(self, educator_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(educator_id), formulas.FIELD("All Educator Record IDs"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, SCHOOLS_TABLE_NAME, formula=formula)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_schools_by_guide_id(self, partner_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Guide Record IDs"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, SCHOOLS_TABLE_NAME, formula=formula)
        return school_models.ListAirtableSchoolResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_guide_school_by_id(self, guide_school_id):
        raw = self.client_api.get(SCHOOLS_BASE_ID, GUIDES_SCHOOLS_TABLE_NAME, guide_school_id)
        return guides_schools_models.AirtableGuidesSchoolsResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def list_partners(self):
        raw = self.client_api.all(SCHOOLS_BASE_ID, PARTNERS_TABLE_NAME)
        return partner_models.ListAirtablePartnerResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_partner_by_id(self, school_id):
        raw = self.client_api.get(SCHOOLS_BASE_ID, PARTNERS_TABLE_NAME, school_id)
        return partner_models.AirtablePartnerResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_partners_by_hub_id(self, hub_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(hub_id), formulas.FIELD("Hub Record ID"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, PARTNERS_TABLE_NAME, formula=formula)
        return partner_models.ListAirtablePartnerResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_partners_by_pod_id(self, pod_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(pod_id), formulas.FIELD("Pod Record ID"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, PARTNERS_TABLE_NAME, formula=formula)
        return partner_models.ListAirtablePartnerResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_partners_by_educator_id(self, educator_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(educator_id), formulas.FIELD("Educator Record IDs"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, PARTNERS_TABLE_NAME, formula=formula)
        return partner_models.ListAirtablePartnerResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_guides_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Guided School Record ID"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, PARTNERS_TABLE_NAME, formula=formula)
        return partner_models.ListAirtablePartnerResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def list_educators(self):
        raw_records = []
        for raw in self.client_api.iterate(SCHOOLS_BASE_ID, EDUCATORS_TABLE_NAME, page_size=10, max_records=10):
            raw_records += raw
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw_records)

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def get_educator_by_id(self, educator_id):
        raw = self.client_api.get(SCHOOLS_BASE_ID, EDUCATORS_TABLE_NAME, educator_id)
        return educator_models.AirtableEducatorResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_educators_by_guide_id(self, partner_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(partner_id), formulas.FIELD("Assigned Partner Record ID"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, EDUCATORS_TABLE_NAME, formula=formula)
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_primary_contacts_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Primary Contact School Record IDs"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, EDUCATORS_TABLE_NAME, formula=formula)
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_all_educators_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("School Record IDs"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, EDUCATORS_TABLE_NAME, formula=formula)
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_current_educators_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Current Educator School Record IDs"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, EDUCATORS_TABLE_NAME, formula=formula)
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_current_tls_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Current TL School Records IDs"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, EDUCATORS_TABLE_NAME, formula=formula)
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=32, ttl=600))
    def get_founders_by_school_id(self, school_id):
        formula = formulas.INCLUDE(formulas.STR_VALUE(school_id), formulas.FIELD("Founder School Records IDs"))

        raw = self.client_api.all(SCHOOLS_BASE_ID, EDUCATORS_TABLE_NAME, formula=formula)
        return educator_models.ListAirtableEducatorResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_educator_school_by_id(self, educator_school_id):
        raw = self.client_api.get(SCHOOLS_BASE_ID, EDUCATORS_SCHOOLS_TABLE_NAME, educator_school_id)
        return educators_schools_models.AirtableEducatorsSchoolsResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_montessori_education_by_id(self, montessori_certification_id):
        raw = self.client_api.get(SCHOOLS_BASE_ID, MONTESSORI_CERTIFICATIONS_TABLE_NAME, montessori_certification_id)
        return montessori_certifications_models.AirtableMontessoriCertificationResponse.parse_obj(raw)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_language_by_id(self, language_id):
        raw = self.client_api.get(SCHOOLS_BASE_ID, LANGUAGES_TABLE_NAME, language_id)
        return languages_models.AirtableLanguageResponse.parse_obj(raw)


def get_airtable_client_generator() -> Generator:
    client = AirtableClient()
    yield client
