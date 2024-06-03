from typing import Callable

from wf_airtable_api_schema.models.partners import *
from wf_airtable_api_schema.models import partners

from . import response as response_models
from . import guides_schools as guides_schools_models
from . import hubs as hubs_model
from . import pods as pods_model
from ..airtable.base_school_db import (
    guides_schools as airtable_guides_schools_models,
    partners as airtable_partner_models,
)


class APIPartnerData(partners.APIPartnerData):
    @classmethod
    def from_airtable_partner(
        cls, airtable_partner: airtable_partner_models.AirtablePartnerResponse, url_path_for: Callable
    ):
        fields = APIPartnerFields(
            name=airtable_partner.fields.name,
            email=airtable_partner.fields.email,
            active=airtable_partner.fields.active,
            active_stint=airtable_partner.fields.active_stint,
            roles=airtable_partner.fields.roles,
        )

        hubs_data = []
        if airtable_partner.fields.hubs is not None:
            for p_id in airtable_partner.fields.hubs:
                hubs_data.append(response_models.APIDataBase(id=p_id, type=hubs_model.MODEL_TYPE))

        pods_data = []
        if airtable_partner.fields.pods is not None:
            for p_id in airtable_partner.fields.pods:
                pods_data.append(response_models.APIDataBase(id=p_id, type=pods_model.MODEL_TYPE))

        guides_schools_data = []
        if airtable_partner.fields.schools_partner_guiding is not None:
            for d in airtable_partner.fields.schools_partner_guiding:
                if isinstance(d, airtable_guides_schools_models.AirtableGuidesSchoolsResponse):
                    guides_schools_data.append(
                        response_models.APIDataWithFields(
                            id=d.id,
                            type=guides_schools_models.MODEL_TYPE,
                            fields=guides_schools_models.APIGuidesSchoolsFields(
                                start_date=d.fields.start_date,
                                end_date=d.fields.end_date,
                                type=d.fields.type,
                                active=d.fields.active,
                                school_id=d.fields.school_id,
                                guide_id=d.fields.guide_id,
                            ),
                        )
                    )
                else:
                    guides_schools_data.append(d)

        educators_partner_guiding_data = []
        if airtable_partner.fields.educators_partner_guiding is not None:
            for e_id in airtable_partner.fields.educators_partner_guiding:
                educators_partner_guiding_data.append(response_models.APIDataBase(id=e_id, type="educators"))

        relationships = APIPartnerRelationships(
            hubs_as_entrepreneur=response_models.APILinksAndData(
                links={"self": url_path_for("get_partner_hubs_as_entrepreneur", partner_id=airtable_partner.id)},
                data=hubs_data,
            ),
            pods_as_contact=response_models.APILinksAndData(
                links={"self": url_path_for("get_partner_pods_as_contact", partner_id=airtable_partner.id)},
                data=pods_data,
            ),
            schools_partner_guiding=response_models.APILinksAndData(
                links={"self": url_path_for("get_guides_schools", partner_id=airtable_partner.id)},
                data=guides_schools_data,
            ),
            educators_partner_guiding=response_models.APILinksAndData(
                links={"self": url_path_for("get_guides_educators", partner_id=airtable_partner.id)},
                data=educators_partner_guiding_data,
            ),
        )
        links = response_models.APILinks(links={"self": url_path_for("get_partner", partner_id=airtable_partner.id)})
        return cls(
            id=airtable_partner.id, type=MODEL_TYPE, fields=fields, relationships=relationships, links=links.links
        )


class ListAPIPartnerData(partners.ListAPIPartnerData):
    @classmethod
    def from_airtable_partners(
        cls, airtable_partners: airtable_partner_models.ListAirtablePartnerResponse, url_path_for: Callable
    ):
        partner_responses = []
        for p in airtable_partners.root:
            partner_responses.append(
                APIPartnerData.from_airtable_partner(airtable_partner=p, url_path_for=url_path_for)
            )

        return cls(root=partner_responses)
