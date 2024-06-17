from typing import Callable

from wf_airtable_api_client.models.auto_response_email_template import *
from wf_airtable_api_client.models import auto_response_email_template

from . import response as response_models
from ..airtable.base_map_by_geographic_area import (
    auto_response_email_template as airtable_auto_response_email_template_models,
)


class APIAutoResponseEmailTemplateData(auto_response_email_template.APIAutoResponseEmailTemplateData):
    @classmethod
    def from_airtable_auto_response_email_template(
        cls,
        airtable_auto_response_email_template: airtable_auto_response_email_template_models.AirtableAutoResponseEmailTemplateResponse,
        url_path_for: Callable,
    ):
        fields = APIAutoResponseEmailTemplateFields(
            geographic_areas=airtable_auto_response_email_template.fields.geographic_areas,
            sendgrid_template_id=airtable_auto_response_email_template.fields.sendgrid_template_id,
            contact_type=airtable_auto_response_email_template.fields.contact_type,
            language=airtable_auto_response_email_template.fields.language,
            first_contact_email=airtable_auto_response_email_template.fields.first_contact_email,
            marketing_source=airtable_auto_response_email_template.fields.marketing_source,
        )

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
            relationships=[],
            links=links.links,
        )


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
