import json
from typing import Callable

from wf_airtable_api_schema.models.geo_area_target_communities import *
from wf_airtable_api_schema.models import geo_area_target_communities

from . import response as response_models
from .response import APIDataBase
from ..airtable.base_map_by_geographic_area import (
    geo_area_target_communities as airtable_geo_area_target_communities_models,
)
from . import hubs as hub_models
from . import target_communities as target_community_models
from ..geocode.geocode_models import Place
from ..geocode.google_maps_client import GoogleMapsAPI


class APIGeoAreaTargetCommunityData(geo_area_target_communities.APIGeoAreaTargetCommunityData):
    @classmethod
    def from_airtable_geo_area_target_community(
        cls,
        airtable_geo_area_target_community: airtable_geo_area_target_communities_models.AirtableGeoAreaTargetCommunityResponse,
        url_path_for: Callable,
    ):

        geocode_dict = None
        if airtable_geo_area_target_community.fields.geocode:
            geocode_dict = json.loads(airtable_geo_area_target_community.fields.geocode)

        fields = APIGeoAreaTargetCommunityFields(
            area_name=airtable_geo_area_target_community.fields.area_name,
            area_type=airtable_geo_area_target_community.fields.area_type,
            city_radius=airtable_geo_area_target_community.fields.city_radius,
            polygon_coordinates=airtable_geo_area_target_community.fields.polygon_coordinates,
            target_community_name=airtable_geo_area_target_community.fields.target_community_name,
            hub_name=airtable_geo_area_target_community.fields.hub_name,
            latitude=airtable_geo_area_target_community.fields.latitude,
            longitude=airtable_geo_area_target_community.fields.longitude,
            geocode=geocode_dict,
        )

        hub_data = None
        if airtable_geo_area_target_community.fields.hub_synced_record_id:
            hub_data = APIDataBase(
                id=airtable_geo_area_target_community.fields.hub_synced_record_id, type=hub_models.MODEL_TYPE
            )

        target_community_data = None
        if airtable_geo_area_target_community.fields.target_community_synced_record_id:
            target_community_data = APIDataBase(
                id=airtable_geo_area_target_community.fields.target_community_synced_record_id,
                type=target_community_models.MODEL_TYPE,
            )

        relationships = APIGeoAreaTargetCommunityRelationships(
            target_community=response_models.APILinksAndData(links=None, data=target_community_data),
        )

        if hub_data is not None:
            relationships.hub = response_models.APILinksAndData(
                links={"self": url_path_for("get_hub", hub_id=hub_data.id)}, data=hub_data
            )

        links = response_models.APILinks(
            links={
                "self": url_path_for(
                    "get_geo_area_target_community", geo_area_target_community_id=airtable_geo_area_target_community.id
                )
            }
        )
        return cls(
            id=airtable_geo_area_target_community.id,
            type=MODEL_TYPE,
            fields=fields,
            relationships=relationships,
            links=links.links,
        )

    def geocode(self):
        if self.fields.geocode is None:
            return GoogleMapsAPI().geocode_address(self.fields.area_name)

        return Place.parse_obj(self.fields.geocode)


class ListAPIGeoAreaTargetCommunityData(geo_area_target_communities.ListAPIGeoAreaTargetCommunityData):
    @classmethod
    def from_airtable_geo_area_target_communities(
        cls,
        airtable_geo_area_target_communities: airtable_geo_area_target_communities_models.ListAirtableGeoAreaTargetCommunityResponse,
        url_path_for: Callable,
    ):
        responses = []
        for lc in airtable_geo_area_target_communities.__root__:
            responses.append(
                APIGeoAreaTargetCommunityData.from_airtable_geo_area_target_community(
                    airtable_geo_area_target_community=lc, url_path_for=url_path_for
                )
            )

        return cls(__root__=responses)
