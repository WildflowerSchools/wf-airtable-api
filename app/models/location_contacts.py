from typing import Callable, Optional

from pydantic import BaseModel

from . import response as response_models
from .response import APIDataBase
from ..airtable.base_start_school_first_contact import location_contacts as airtable_location_contacts_models
from . import hubs as hub_models
from . import partners as partner_models

MODEL_TYPE = 'location_contacts'


class APILocationContactFields(BaseModel):
    location: Optional[str] = None
    location_type: Optional[str] = None
    city_radius: Optional[int] = None
    first_contact_email: Optional[str] = None
    assigned_rse_name: Optional[str] = None
    hub_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class APILocationContactRelationships(BaseModel):
    hub: Optional[response_models.APILinksAndData] = None
    assigned_rse: Optional[response_models.APILinksAndData] = None


class APILocationContactData(response_models.APIData):
    fields: APILocationContactFields

    @classmethod
    def from_airtable_location_contact(cls,
                                       airtable_location_contact: airtable_location_contacts_models.AirtableLocationContactResponse,
                                       url_path_for: Callable):
        fields = APILocationContactFields(
            location=airtable_location_contact.fields.location,
            location_type=airtable_location_contact.fields.location_type,
            city_radius=airtable_location_contact.fields.city_radius,
            first_contact_email=airtable_location_contact.fields.first_contact_email,
            assigned_rse_name=airtable_location_contact.fields.assigned_rse_name,
            hub_name=airtable_location_contact.fields.hub_name,
            latitude=airtable_location_contact.fields.latitude,
            longitude=airtable_location_contact.fields.longitude)

        hub_data = None
        if airtable_location_contact.fields.hub:
            hub_data = APIDataBase(
                id=airtable_location_contact.fields.hub,
                type=hub_models.MODEL_TYPE)

        rse_data = None
        if airtable_location_contact.fields.hub:
            rse_data = APIDataBase(
                id=airtable_location_contact.fields.assigned_rse,
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
        return response_models.APIData(
            id=airtable_location_contact.id,
            type=MODEL_TYPE,
            fields=fields,
            relationships=relationships,
            links=links.links
        )


class ListAPILocationContactData(BaseModel):
    __root__: list[APILocationContactData]

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
