from typing import Callable

from wf_airtable_api_schema.models.pods import *
from wf_airtable_api_schema.models import pods

from . import response as response_models
from .response import APIDataBase
from ..airtable.base_school_db import pods as airtable_pod_models
from . import hubs as hub_models
from . import partners as partner_models
from . import schools as school_models


class APIPodData(pods.APIPodData):
    @classmethod
    def from_airtable_pod(cls, airtable_pod: airtable_pod_models.AirtablePodResponse, url_path_for: Callable):
        fields = APIPodFields(name=airtable_pod.fields.name)

        hub_data = None
        if airtable_pod.fields.hub:
            hub_data = APIDataBase(id=airtable_pod.fields.hub, type=hub_models.MODEL_TYPE)

        pod_contacts_data = []
        if airtable_pod.fields.pod_contacts is not None:
            for pc_id in airtable_pod.fields.pod_contacts:
                pod_contacts_data.append(APIDataBase(id=pc_id, type=partner_models.MODEL_TYPE))

        schools_data = []
        if airtable_pod.fields.schools is not None:
            for s_id in airtable_pod.fields.schools:
                schools_data.append(APIDataBase(id=s_id, type=school_models.MODEL_TYPE))

        relationships = APIPodRelationships(
            hub=response_models.APILinksAndData(
                links={"self": url_path_for("get_pod_hub", pod_id=airtable_pod.id)}, data=hub_data
            ),
            pod_contacts=response_models.APILinksAndData(
                links={"self": url_path_for("get_pod_contacts", pod_id=airtable_pod.id)}, data=pod_contacts_data
            ),
            schools=response_models.APILinksAndData(
                links={"self": url_path_for("get_pod_schools", pod_id=airtable_pod.id)}, data=schools_data
            ),
        )
        links = response_models.APILinks(links={"self": url_path_for("get_pod", pod_id=airtable_pod.id)})
        return cls(id=airtable_pod.id, type=MODEL_TYPE, fields=fields, relationships=relationships, links=links.links)


class ListAPIPodData(pods.ListAPIPodData):
    @classmethod
    def from_airtable_pods(cls, airtable_pods: airtable_pod_models.ListAirtablePodResponse, url_path_for: Callable):
        pod_responses = []
        for p in airtable_pods.__root__:
            pod_responses.append(APIPodData.from_airtable_pod(airtable_pod=p, url_path_for=url_path_for))

        return cls(__root__=pod_responses)
