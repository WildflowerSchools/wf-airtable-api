from typing import Callable

from wf_airtable_api_schema.models.hubs import *
from wf_airtable_api_schema.models import hubs


from . import response as response_models
from .response import APIDataBase
from ..airtable.base_school_db import hubs as airtable_hub_models
from . import partners as partner_models
from . import pods as pod_models
from . import schools as school_models


class APIHubData(hubs.APIHubData):
    @classmethod
    def from_airtable_hub(cls, airtable_hub: airtable_hub_models.AirtableHubResponse, url_path_for: Callable):
        fields = APIHubFields(name=airtable_hub.fields.name)

        regional_site_entrepreneurs_data = []
        if airtable_hub.fields.regional_site_entrepreneurs is not None:
            for rs_id in airtable_hub.fields.regional_site_entrepreneurs:
                regional_site_entrepreneurs_data.append(APIDataBase(id=rs_id, type=partner_models.MODEL_TYPE))

        pods_data = []
        if airtable_hub.fields.pods is not None:
            for p_id in airtable_hub.fields.pods:
                pods_data.append(APIDataBase(id=p_id, type=pod_models.MODEL_TYPE))

        schools_data = []
        if airtable_hub.fields.schools is not None:
            for s_id in airtable_hub.fields.schools:
                schools_data.append(APIDataBase(id=s_id, type=school_models.MODEL_TYPE))

        relationships = APIHubRelationships(
            regional_site_entrepreneurs=response_models.APILinksAndData(
                links={"self": url_path_for("get_hub_site_entrepreneurs", hub_id=airtable_hub.id)},
                data=regional_site_entrepreneurs_data,
            ),
            pods=response_models.APILinksAndData(
                links={"self": url_path_for("get_hub_pods", hub_id=airtable_hub.id)}, data=pods_data
            ),
            schools=response_models.APILinksAndData(
                links={"self": url_path_for("get_hub_schools", hub_id=airtable_hub.id)}, data=schools_data
            ),
        )
        links = response_models.APILinks(links={"self": url_path_for("get_hub", hub_id=airtable_hub.id)})
        return cls(id=airtable_hub.id, type=MODEL_TYPE, fields=fields, relationships=relationships, links=links.links)


class ListAPIHubData(hubs.ListAPIHubData):
    @classmethod
    def from_airtable_hubs(cls, airtable_hubs: airtable_hub_models.ListAirtableHubResponse, url_path_for: Callable):
        hub_responses = []
        for h in airtable_hubs.root:
            hub_responses.append(APIHubData.from_airtable_hub(airtable_hub=h, url_path_for=url_path_for))

        return cls(root=hub_responses)
