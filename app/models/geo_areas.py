import json
from typing import Callable

from wf_airtable_api_client.models.geo_areas import *
from wf_airtable_api_client.models import geo_areas

from . import response as response_models
from .response import APIDataBase, APIDataWithFields
from ..airtable.base_map_by_geographic_area import geo_areas as airtable_geo_areas_models
from . import auto_response_email_template as auto_response_email_template_models
from . import hubs as hub_models
from . import partners as partner_models
from ..geocode.geocode_models import Place
from ..geocode.google_maps_client import GoogleMapsAPI


class APIGeoAreaData(geo_areas.APIGeoAreaData):
    @classmethod
    def from_airtable_geo_area(
        cls,
        airtable_geo_area: airtable_geo_areas_models.AirtableGeoAreaResponse,
        url_path_for: Callable,
    ):
        from ..airtable.client import AirtableClient

        airtable_client = AirtableClient()

        geocode_dict = None
        if airtable_geo_area.fields.geocode:
            geocode_dict = json.loads(airtable_geo_area.fields.geocode)

        fields = APIGeoAreaFields(
            area_name=airtable_geo_area.fields.area_name,
            area_type=airtable_geo_area.fields.area_type,
            city_radius=airtable_geo_area.fields.city_radius,
            polygon_coordinates=airtable_geo_area.fields.polygon_coordinates,
            assigned_rse_name=airtable_geo_area.fields.assigned_rse_name,
            hub_name=airtable_geo_area.fields.hub_name,
            latitude=airtable_geo_area.fields.latitude,
            longitude=airtable_geo_area.fields.longitude,
            geocode=geocode_dict,
            auto_response_email_templates=airtable_geo_area.fields.auto_response_email_templates,
        )

        hub_data = None
        if airtable_geo_area.fields.hub_synced_record_id:
            hub_data = APIDataBase(id=airtable_geo_area.fields.hub_synced_record_id, type=hub_models.MODEL_TYPE)

        rse_link = None
        if airtable_geo_area.fields.assigned_rse_synced_record_id:
            # The Partner table is in its own base and it's referenced by multiple other bases
            # However, the Record IDs are unique to each base. So lookup needs to be performed to
            # translate Record IDs between bases
            partner_record = airtable_client.get_partner_by_synced_record_id(
                airtable_geo_area.fields.assigned_rse_synced_record_id
            )

            rse_data = APIDataBase(id=partner_record.id, type=partner_models.MODEL_TYPE)
            rse_link = response_models.APILinksAndData(
                links={"self": url_path_for("get_partner", partner_id=rse_data.id)}, data=rse_data
            )

        hub_link = None
        if hub_data and hasattr(hub_data, "id"):
            hub_link = response_models.APILinksAndData(
                links={"self": url_path_for("get_hub", hub_id=hub_data.id)}, data=hub_data
            )

        auto_response_template_links = []
        if airtable_geo_area.fields.auto_response_email_templates:
            for auto_response_template_id in airtable_geo_area.fields.auto_response_email_templates:
                auto_response_template_record = airtable_client.get_auto_response_email_template_by_id(
                    auto_response_template_id
                )
                auto_response_template_data = APIDataWithFields(
                    id=auto_response_template_record.id,
                    type=auto_response_email_template_models.MODEL_TYPE,
                    fields=auto_response_template_record.fields,
                )
                auto_response_template_links.append(
                    response_models.APILinksAndData(
                        links={
                            "self": url_path_for(
                                "get_auto_response_email_template",
                                auto_response_email_template_id=auto_response_template_data.id,
                            )
                        },
                        data=auto_response_template_data,
                    )
                )

        relationships = APIGeoAreaRelationships(
            hub=hub_link, assigned_rse=rse_link, auto_response_email_templates=auto_response_template_links
        )
        links = response_models.APILinks(links={"self": url_path_for("get_geo_area", geo_area_id=airtable_geo_area.id)})
        return cls(
            id=airtable_geo_area.id,
            type=MODEL_TYPE,
            fields=fields,
            relationships=relationships,
            links=links.links,
        )

    def geocode(self):
        if self.fields.geocode is None:
            return GoogleMapsAPI().geocode_address(self.fields.area_name)

        return Place.parse_obj(self.fields.geocode)


class ListAPIGeoAreaData(geo_areas.ListAPIGeoAreaData):
    @classmethod
    def from_airtable_geo_areas(
        cls,
        airtable_geo_areas: airtable_geo_areas_models.ListAirtableGeoAreaResponse,
        url_path_for: Callable,
    ):
        responses = []
        for gac in airtable_geo_areas.root:
            responses.append(APIGeoAreaData.from_airtable_geo_area(airtable_geo_area=gac, url_path_for=url_path_for))

        return cls(root=responses)
