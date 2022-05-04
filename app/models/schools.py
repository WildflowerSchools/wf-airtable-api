from typing import Callable

from wf_airtable_api_schema.models.schools import *
from wf_airtable_api_schema.models import schools

from . import response as response_models
from . import educators as educator_models
from . import hubs as hub_models
from . import partners as partner_models
from . import pods as pod_models
from ..airtable.base_school_db import schools as airtable_school_models


class APISchoolData(schools.APISchoolData):
    @classmethod
    def from_airtable_school(
        cls, airtable_school: airtable_school_models.AirtableSchoolResponse, url_path_for: Callable
    ):
        fields = APISchoolFields(
            name=airtable_school.fields.name,
            short_name=airtable_school.fields.short_name,
            details=airtable_school.fields.details,
            logo_url=airtable_school.fields.get_logo_url(),
            domain_name=airtable_school.fields.domain_name,
            address=airtable_school.fields.address,
            latitude=airtable_school.fields.latitude,
            longitude=airtable_school.fields.longitude,
            organizational_unit=airtable_school.fields.organizational_unit,
            hub_name=airtable_school.fields.hub_name,
            pod_name=airtable_school.fields.pod_name,
            ages_served=airtable_school.fields.ages_served,
            school_calendar=airtable_school.fields.school_calendar,
            school_schedule=airtable_school.fields.school_schedule,
            school_phone=airtable_school.fields.school_phone,
            school_email=airtable_school.fields.school_email,
            website=airtable_school.fields.website,
            status=airtable_school.fields.status,
            ssj_stage=airtable_school.fields.ssj_stage,
            began_ssj_at=airtable_school.fields.began_ssj_at,
            entered_planning_at=airtable_school.fields.entered_planning_at,
            entered_startup_at=airtable_school.fields.entered_startup_at,
            opened_at=airtable_school.fields.opened_at,
            projected_open=airtable_school.fields.projected_open,
            affiliation_status=airtable_school.fields.affiliation_status,
            affiliated_at=airtable_school.fields.affiliated_at,
            affiliation_agreement_url=airtable_school.fields.get_affiliation_agreement_url(),
            nonprofit_status=airtable_school.fields.nonprofit_status,
            left_network_reason=airtable_school.fields.left_network_reason,
            left_network_date=airtable_school.fields.left_network_date,
        )

        hub_data = None
        if airtable_school.fields.hub:
            hub_data = response_models.APIDataBase(id=airtable_school.fields.hub, type=hub_models.MODEL_TYPE)

        pod_data = None
        if airtable_school.fields.pod:
            pod_data = response_models.APIDataBase(id=airtable_school.fields.pod, type=pod_models.MODEL_TYPE)

        guides_and_entrepreneurs_data = []
        if airtable_school.fields.guides_entrepreneurs is not None:
            for ge_id in airtable_school.fields.guides_entrepreneurs:
                guides_and_entrepreneurs_data.append(
                    response_models.APIDataBase(id=ge_id, type=partner_models.MODEL_TYPE)
                )

        primary_contacts_data = []
        if airtable_school.fields.primary_contacts is not None:
            for e_id in airtable_school.fields.primary_contacts:
                primary_contacts_data.append(response_models.APIDataBase(id=e_id, type=educator_models.MODEL_TYPE))

        all_educators_data = []
        if airtable_school.fields.all_educators is not None:
            for e_id in airtable_school.fields.all_educators:
                all_educators_data.append(response_models.APIDataBase(id=e_id, type=educator_models.MODEL_TYPE))

        current_educators_data = []
        if airtable_school.fields.current_educators is not None:
            for e_id in airtable_school.fields.current_educators:
                current_educators_data.append(response_models.APIDataBase(id=e_id, type=educator_models.MODEL_TYPE))

        current_tls_data = []
        if airtable_school.fields.current_tls is not None:
            for e_id in airtable_school.fields.current_tls:
                current_tls_data.append(response_models.APIDataBase(id=e_id, type=educator_models.MODEL_TYPE))

        founders_data = []
        if airtable_school.fields.founders is not None:
            for e_id in airtable_school.fields.founders:
                founders_data.append(response_models.APIDataBase(id=e_id, type=educator_models.MODEL_TYPE))

        relationships = APISchoolRelationships(
            hub=response_models.APILinksAndData(
                links={"self": url_path_for("get_school_hub", school_id=airtable_school.id)}, data=hub_data
            ),
            pod=response_models.APILinksAndData(
                links={"self": url_path_for("get_school_pod", school_id=airtable_school.id)}, data=pod_data
            ),
            guides_and_entrepreneurs=response_models.APILinksAndData(
                links={"self": url_path_for("get_school_guides_and_entrepreneurs", school_id=airtable_school.id)},
                data=guides_and_entrepreneurs_data,
            ),
            primary_contacts=response_models.APILinksAndData(
                links={"self": url_path_for("get_school_primary_contacts", school_id=airtable_school.id)},
                data=primary_contacts_data,
            ),
            educators=response_models.APILinksAndData(
                links={"self": url_path_for("get_school_educators", school_id=airtable_school.id)},
                data=all_educators_data,
            ),
            current_educators=response_models.APILinksAndData(
                links={"self": url_path_for("get_school_current_educators", school_id=airtable_school.id)},
                data=current_educators_data,
            ),
            current_tls=response_models.APILinksAndData(
                links={"self": url_path_for("get_school_current_tls", school_id=airtable_school.id)},
                data=current_tls_data,
            ),
            founders=response_models.APILinksAndData(
                links={"self": url_path_for("get_school_founders", school_id=airtable_school.id)}, data=founders_data
            ),
        )
        links = response_models.APILinks(links={"self": url_path_for("get_school", school_id=airtable_school.id)})
        return cls(
            id=airtable_school.id, type=MODEL_TYPE, fields=fields, relationships=relationships, links=links.links
        )


class ListAPISchoolData(schools.ListAPISchoolData):
    @classmethod
    def from_airtable_schools(
        cls, airtable_schools: airtable_school_models.ListAirtableSchoolResponse, url_path_for: Callable
    ):

        school_responses = []
        for s in airtable_schools.__root__:
            school_responses.append(APISchoolData.from_airtable_school(airtable_school=s, url_path_for=url_path_for))

        return cls(__root__=school_responses)
