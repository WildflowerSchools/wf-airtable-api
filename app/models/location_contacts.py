import time

from typing import Callable, Optional

from pydantic import BaseModel

from wf_airtable_api_schema.models.location_contacts import *
from wf_airtable_api_schema.models import location_contacts

from . import response as response_models
from .response import APIDataBase
from ..airtable.base_start_school_first_contact import location_contacts as airtable_location_contacts_models
from . import hubs as hub_models
from . import partners as partner_models
from ..geocode.google_maps_client import GoogleMapsAPI


class APILocationContactData(location_contacts.APILocationContactData):
    @classmethod
    def from_airtable_location_contact(cls,
                                       airtable_location_contact: airtable_location_contacts_models.AirtableLocationContactResponse,
                                       url_path_for: Callable):
        from ..airtable.client import AirtableClient
        airtable_client = AirtableClient()

        fields = APILocationContactFields(
            location=airtable_location_contact.fields.location,
            location_type=airtable_location_contact.fields.location_type,
            city_radius=airtable_location_contact.fields.city_radius,
            first_contact_email=airtable_location_contact.fields.first_contact_email,
            assigned_rse_name=airtable_location_contact.fields.assigned_rse_name,
            hub_name=airtable_location_contact.fields.hub_name,
            sendgrid_template_id=airtable_location_contact.fields.sendgrid_template_id,
            latitude=airtable_location_contact.fields.latitude,
            longitude=airtable_location_contact.fields.longitude)

        hub_data = None
        if airtable_location_contact.fields.hub_synced_record_id:
            hub_data = APIDataBase(
                id=airtable_location_contact.fields.hub_synced_record_id,
                type=hub_models.MODEL_TYPE)

        rse_data = None
        if airtable_location_contact.fields.assigned_rse_synced_record_id:
            # The Partner table is in its own base and it's referenced by multiple other bases
            # However, the Record IDs are unique to each base. So lookup needs to be performed to
            # translate Record IDs between bases
            partner_record = airtable_client.get_partner_by_synced_record_id(
                airtable_location_contact.fields.assigned_rse_synced_record_id)

            rse_data = APIDataBase(
                id=partner_record.id,
                type=partner_models.MODEL_TYPE)

        relationships = APILocationContactRelationships(
            hub=response_models.APILinksAndData(
                links={'self': url_path_for("get_hub", hub_id=hub_data.id)},
                data=hub_data),
            assigned_rse=response_models.APILinksAndData(
                links={'self': url_path_for("get_partner", partner_id=rse_data.id)},
                data=rse_data),
        )
        links = response_models.APILinks(
            links={'self': url_path_for("get_location_contact", location_contact_id=airtable_location_contact.id)}
        )
        return cls(
            id=airtable_location_contact.id,
            type=MODEL_TYPE,
            fields=fields,
            relationships=relationships,
            links=links.links
        )

    def geocode(self):
        return GoogleMapsAPI().geocode_address(self.fields.location)


class ListAPILocationContactData(location_contacts.ListAPILocationContactData):
    @classmethod
    def from_airtable_location_contacts(cls,
                                        airtable_location_contacts: airtable_location_contacts_models.ListAirtableLocationContactResponse,
                                        url_path_for: Callable):
        responses = []
        for lc in airtable_location_contacts.__root__:
            responses.append(
                APILocationContactData.from_airtable_location_contact(
                    airtable_location_contact=lc,
                    url_path_for=url_path_for))

        return cls(__root__=responses)
