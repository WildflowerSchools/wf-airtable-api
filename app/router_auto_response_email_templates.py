import requests
from fastapi import APIRouter, Depends, Request, HTTPException

from .airtable.client import AirtableClient
from .models import auto_response_email_template as auto_response_email_template_models
from .models import hubs as hub_models
from .models import partners as partner_models
from . import auth
from .utils.utils import get_airtable_client

OPENAPI_TAG_METADATA = {"name": auto_response_email_template_models.MODEL_TYPE, "description": "Auto-response email mapping data"}

router = APIRouter(
    prefix="/auto_response_email_templates",
    tags=[auto_response_email_template_models.MODEL_TYPE],
    dependencies=[Depends(auth.JWTBearer(any_scope=["read:all", "read:educators", "read:schools"]))],
    responses={404: {"description": "Not found"}},
)


def fetch_auto_response_email_template_wrapper(auto_response_email_template_id, airtable_client: AirtableClient):
    try:
        airtable_auto_response_email_template = airtable_client.get_auto_response_email_template_by_id(auto_response_email_template_id)
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Auto-Response Email Template not found")
        else:
            raise

    return airtable_auto_response_email_template


# Dupe the root route to solve this issue: https://github.com/tiangolo/fastapi/issues/2060
@router.get("/", response_model=auto_response_email_template_models.ListAPIAutoResponseEmailTemplateResponse, include_in_schema=False)
@router.get("", response_model=auto_response_email_template_models.ListAPIAutoResponseEmailTemplateResponse)
async def list_auto_response_email_templates(request: Request):
    airtable_client = get_airtable_client(request)
    airtable_auto_response_templates = airtable_client.list_auto_response_email_templates()

    data = auto_response_email_template_models.ListAPIGeoAreaTargetCommunityData.from_airtable_geo_area_target_communities(
        airtable_auto_response_email_templates=airtable_auto_response_templates, url_path_for=request.app.url_path_for
    ).__root__

    return auto_response_email_template_models.ListAPIAutoResponseEmailTemplateResponse(data=data, links={"self": request.app.url_path_for("list_auto_response_email_templates")})


@router.get("/{auto_response_email_template_id}", response_model=auto_response_email_template_models.APIAutoResponseEmailTemplateResponse)
async def get_auto_response_email_template(auto_response_email_template_id, request: Request):
    airtable_client = get_airtable_client(request)
    airtable_auto_response_email_template = fetch_auto_response_email_template_wrapper(auto_response_email_template_id, airtable_client)

    data = auto_response_email_template_models.APIAutoResponseEmailTemplateData.from_airtable_auto_response_email_template(airtable_auto_response_email_template=airtable_auto_response_email_template, url_path_for=request.app.url_path_for)

    return auto_response_email_template_models.APIAutoResponseEmailTemplateResponse(data=data, links={"self": request.app.url_path_for("get_auto_response_email_template", auto_response_email_template_id=auto_response_email_template_id)})

#
# @router.get("/{auto_response_email_template_id}/hub", response_model=hub_models.APIHubResponse)
# async def get_auto_response_email_template_site_entrepreneur_hub(auto_response_email_template_id, request: Request):
#     airtable_client = get_airtable_client(request)
#     airtable_auto_response_email_template = fetch_auto_response_email_template_wrapper(auto_response_email_template_id, airtable_client)
#     airtable_hub = airtable_client.get_hub_by_id(hub_id=airtable_auto_response_email_template.fields.hub_synced_record_id)
#
#     data = hub_models.APIHubData.from_airtable_hub(airtable_hub=airtable_hub, url_path_for=request.app.url_path_for)
#
#     return hub_models.APIHubResponse(data=data, links={"self": request.app.url_path_for("get_auto_response_email_template_site_entrepreneur_hub", auto_response_email_template_id=auto_response_email_template_id)})
#
#
# @router.get("/{auto_response_email_template_id}/regional_site_entrepreneur", response_model=partner_models.APIPartnerResponse)
# async def get_auto_response_email_template_site_entrepreneur(auto_response_email_template_id, request: Request):
#     airtable_client = get_airtable_client(request)
#     airtable_auto_response_email_template = fetch_auto_response_email_template_wrapper(auto_response_email_template_id, airtable_client)
#     airtable_assigned_rse = airtable_client.get_partner_by_synced_record_id(airtable_auto_response_email_template.fields.assigned_rse_synced_record_id)
#
#     data = partner_models.APIPartnerData.from_airtable_partner(
#         airtable_partner=airtable_assigned_rse, url_path_for=request.app.url_path_for
#     )
#
#     return partner_models.APIPartnerResponse(
#         data=data, links={"self": request.app.url_path_for("get_auto_response_email_template_site_entrepreneur", auto_response_email_template_id=auto_response_email_template_id)}
#     )
