import json
from typing import Callable

from wf_airtable_api_schema.models.geo_area_contacts import *
from wf_airtable_api_schema.models import geo_area_contacts

from . import response as response_models
from .response import APIDataBase
from ..airtable.base_map_by_geographic_area import geo_area_contacts as airtable_geo_area_contacts_models
from . import hubs as hub_models
from . import partners as partner_models
from ..geocode.geocode_models import Place
from ..geocode.google_maps_client import GoogleMapsAPI


class APIGeoAreaContactData(geo_area_contacts.APIGeoAreaContactData):
    @classmethod
    def from_airtable_geo_area_contact(
        cls,
        airtable_geo_area_contact: airtable_geo_area_contacts_models.AirtableGeoAreaContactResponse,
        url_path_for: Callable,
    ):
        from ..airtable.client import AirtableClient

        airtable_client = AirtableClient()

        geocode_dict = None
        if airtable_geo_area_contact.fields.geocode:
            geocode_dict = json.loads(airtable_geo_area_contact.fields.geocode)

        fields = APIGeoAreaContactFields(
            area_name=airtable_geo_area_contact.fields.area_name,
            area_type=airtable_geo_area_contact.fields.area_type,
            city_radius=airtable_geo_area_contact.fields.city_radius,
            polygon_coordinates=airtable_geo_area_contact.fields.polygon_coordinates,
            first_contact_email=airtable_geo_area_contact.fields.first_contact_email,
            assigned_rse_name=airtable_geo_area_contact.fields.assigned_rse_name,
            hub_name=airtable_geo_area_contact.fields.hub_name,
            sendgrid_template_id=airtable_geo_area_contact.fields.sendgrid_template_id,
            latitude=airtable_geo_area_contact.fields.latitude,
            longitude=airtable_geo_area_contact.fields.longitude,
            geocode=geocode_dict,
        )

        hub_data = None
        if airtable_geo_area_contact.fields.hub_synced_record_id:
            hub_data = APIDataBase(id=airtable_geo_area_contact.fields.hub_synced_record_id, type=hub_models.MODEL_TYPE)

        rse_data = None
        if airtable_geo_area_contact.fields.assigned_rse_synced_record_id:
            # The Partner table is in its own base and it's referenced by multiple other bases
            # However, the Record IDs are unique to each base. So lookup needs to be performed to
            # translate Record IDs between bases
            partner_record = airtable_client.get_partner_by_synced_record_id(
                airtable_geo_area_contact.fields.assigned_rse_synced_record_id
            )

            rse_data = APIDataBase(id=partner_record.id, type=partner_models.MODEL_TYPE)

        hub_link = None
        if hub_data and "id" in hub_data:
            hub_link = response_models.APILinksAndData(
                links={"self": url_path_for("get_hub", hub_id=hub_data.id)}, data=hub_data
            )

        relationships = APIGeoAreaContactRelationships(
            hub=hub_link,
            assigned_rse=response_models.APILinksAndData(
                links={"self": url_path_for("get_partner", partner_id=rse_data.id)}, data=rse_data
            ),
        )
        links = response_models.APILinks(
            links={"self": url_path_for("get_geo_area_contact", geo_area_contact_id=airtable_geo_area_contact.id)}
        )
        return cls(
            id=airtable_geo_area_contact.id,
            type=MODEL_TYPE,
            fields=fields,
            relationships=relationships,
            links=links.links,
        )

    def geocode(self):
        if self.fields.geocode is None:
            return GoogleMapsAPI().geocode_address(self.fields.area_name)

        return Place.parse_obj(self.fields.geocode)


class ListAPIGeoAreaContactData(geo_area_contacts.ListAPIGeoAreaContactData):
    @classmethod
    def from_airtable_geo_area_contacts(
        cls,
        airtable_geo_area_contacts: airtable_geo_area_contacts_models.ListAirtableGeoAreaContactResponse,
        url_path_for: Callable,
    ):
        responses = []
        for lc in airtable_geo_area_contacts.__root__:
            responses.append(
                APIGeoAreaContactData.from_airtable_geo_area_contact(
                    airtable_geo_area_contact=lc, url_path_for=url_path_for
                )
            )

        return cls(__root__=responses)
