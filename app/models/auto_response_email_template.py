import json
from typing import Callable

from wf_airtable_api_schema.models.auto_response_email_template import *
from wf_airtable_api_schema.models import auto_response_email_template

from . import response as response_models
from .response import APIDataBase
from ..airtable.base_map_by_geographic_area import (
    auto_response_email_template as airtable_auto_response_email_template_models,
)
from . import hubs as hub_models

# from . import partners as partner_models
# from ..geocode.geocode_models import Place
# from ..geocode.google_maps_client import GoogleMapsAPI


class APIAutoResponseEmailTemplateData(auto_response_email_template.APIAutoResponseEmailTemplateData):
    @classmethod
    def from_airtable_auto_response_email_template(
        cls,
        airtable_auto_response_email_template: airtable_auto_response_email_template_models.AirtableAutoResponseEmailTemplateResponse,
        url_path_for: Callable,
    ):
        from ..airtable.client import AirtableClient

        # airtable_client = AirtableClient()
        #
        # geocode_dict = None
        # if airtable_auto_response_email_template.fields.geocode:
        #     geocode_dict = json.loads(airtable_auto_response_email_template.fields.geocode)

        fields = APIAutoResponseEmailTemplateFields(
            # area_contacts=airtable_auto_response_email_template.fields.area_contacts,
            geographic_areas=airtable_auto_response_email_template.fields.geographic_areas,
            sendgrid_template_id=airtable_auto_response_email_template.fields.sendgrid_template_id,
            contact_type=airtable_auto_response_email_template.fields.contact_type,
            language=airtable_auto_response_email_template.fields.language,
            # area_name=airtable_auto_response_email_template.fields.area_name,
            # area_type=airtable_auto_response_email_template.fields.area_type,
            # city_radius=airtable_auto_response_email_template.fields.city_radius,
            # polygon_coordinates=airtable_auto_response_email_template.fields.polygon_coordinates,
            first_contact_email=airtable_auto_response_email_template.fields.first_contact_email,
            # assigned_rse_name=airtable_auto_response_email_template.fields.assigned_rse_name,
            # hub_name=airtable_auto_response_email_template.fields.hub_name,
            # latitude=airtable_auto_response_email_template.fields.latitude,
            # longitude=airtable_auto_response_email_template.fields.longitude,
            # geocode=geocode_dict,
        )

        # hub_data = None
        # if airtable_auto_response_email_template.fields.hub_synced_record_id:
        #     hub_data = APIDataBase(
        #         id=airtable_auto_response_email_template.fields.hub_synced_record_id, type=hub_models.MODEL_TYPE
        #     )

        # hub_link = None
        # if hub_data is not None:
        #     hub_link = response_models.APILinksAndData(
        #         links={"self": url_path_for("get_hub", hub_id=hub_data.id)}, data=hub_data
        #     )
        #
        # rse_data = None
        # if airtable_auto_response_email_template.fields.assigned_rse_synced_record_id:
        #     # The Partner table is in its own base and it's referenced by multiple other bases
        #     # However, the Record IDs are unique to each base. So lookup needs to be performed to
        #     # translate Record IDs between bases
        #     partner_record = airtable_client.get_partner_by_synced_record_id(
        #         airtable_auto_response_email_template.fields.assigned_rse_synced_record_id
        #     )
        #
        #     rse_data = APIDataBase(id=partner_record.id, type=partner_models.MODEL_TYPE)
        #
        # relationships = APIAutoResponseEmailTemplateRelationships(
        #     hub=hub_link,
        #     assigned_rse=response_models.APILinksAndData(
        #         links={"self": url_path_for("get_partner", partner_id=rse_data.id)}, data=rse_data
        #     ),
        # )

        links = response_models.APILinks(
            links={
                "self": url_path_for(
                    "get_auto_response_email_template",
                    auto_response_email_template_id=airtable_auto_response_email_template.id,
                )
            }
        )
        return cls(
            id=airtable_auto_response_email_template.id,
            type=MODEL_TYPE,
            fields=fields,
            relationships=[],  # relationships,
            links=links.links,
        )

    # def geocode(self):
    #     if self.fields.geocode is None:
    #         return GoogleMapsAPI().geocode_address(self.fields.area_name)
    #
    #     return Place.parse_obj(self.fields.geocode)


class ListAPIAutoResponseEmailTemplateData(auto_response_email_template.ListAPIAutoResponseEmailTemplateData):
    @classmethod
    def from_airtable_auto_response_email_templates(
        cls,
        airtable_auto_response_email_templates: airtable_auto_response_email_template_models.ListAirtableAutoResponseEmailTemplateResponse,
        url_path_for: Callable,
    ) -> ListAPIAutoResponseEmailTemplateData:
        responses = []
        for aet in airtable_auto_response_email_templates.root:
            responses.append(
                APIAutoResponseEmailTemplateData.from_airtable_auto_response_email_template(
                    airtable_auto_response_email_template=aet, url_path_for=url_path_for
                )
            )

        return cls(root=responses)
