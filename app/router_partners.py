import requests
from fastapi import APIRouter, Depends, HTTPException, Request

from .airtable.client import AirtableClient
from .models import response as response_models
from .models import educators as educator_models
from .models import hubs as hub_models
from .models import partners as partner_models
from .models import pods as pod_models
from .models import schools as school_models
from . import auth

router = APIRouter(
    prefix="/partners",
    tags=[partner_models.MODEL_TYPE],
    dependencies=[Depends(auth.JWTBearer(any_scope=['read:all', 'read:partners']))],
    responses={404: {"description": "Not found"}}
)


def fetch_and_validate_partner(partner_id, airtable_client: AirtableClient):
    try:
        airtable_partner = airtable_client.get_partner_by_id(partner_id)
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Partner not found")
        else:
            raise

    return airtable_partner


# Dupe the root route to solve this issue: https://github.com/tiangolo/fastapi/issues/2060
@router.get("/", response_model=response_models.ListAPIResponse, include_in_schema=False)
@router.get("", response_model=response_models.ListAPIResponse)
async def list_partners(request: Request):
    airtable_client = request.state.airtable_client
    airtable_partners = airtable_client.list_partners()

    return partner_models.ListAPIPartnerResponse.from_airtable_partners(
        airtable_partners=airtable_partners,
        url_path_for=request.app.url_path_for)


@router.get("/{partner_id}", response_model=response_models.APIResponse)
async def get_partner(partner_id, request: Request):
    airtable_client = request.state.airtable_client
    airtable_partner = fetch_and_validate_partner(partner_id, airtable_client)

    return partner_models.APIPartnerResponse.from_airtable_partner(
        airtable_partner=airtable_partner,
        url_path_for=request.app.url_path_for)


@router.get("/{partner_id}/hubs_as_entrepreneur", response_model=response_models.ListAPIResponse)
async def get_partner_hubs_as_entrepreneur(partner_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_partner(partner_id, airtable_client)
    airtable_hubs = airtable_client.get_hubs_by_entrepreneur_id(partner_id)

    return hub_models.ListAPIHubResponse.from_airtable_hubs(
        airtable_hubs=airtable_hubs,
        url_path_for=request.app.url_path_for)


@router.get("/{partner_id}/pods_as_contact", response_model=response_models.ListAPIResponse)
async def get_partner_pods_as_contact(partner_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_partner(partner_id, airtable_client)
    airtable_pods = airtable_client.get_pods_by_contact_id(partner_id)

    return pod_models.ListAPIPodResponse.from_airtable_pods(
        airtable_pods=airtable_pods,
        url_path_for=request.app.url_path_for)


@router.get("/{partner_id}/schools_guiding", response_model=response_models.ListAPIResponse)
async def get_guides_schools(partner_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_partner(partner_id, airtable_client)
    airtable_schools = airtable_client.get_schools_by_guide_id(partner_id)

    return school_models.ListAPISchoolResponse.from_airtable_schools(
        airtable_schools=airtable_schools,
        url_path_for=request.app.url_path_for)


@router.get("/{partner_id}/educators_guiding", response_model=response_models.ListAPIResponse)
async def get_guides_educators(partner_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_partner(partner_id, airtable_client)
    airtable_educators = airtable_client.get_educators_by_guide_id(partner_id)

    return educator_models.ListAPIEducatorResponse.from_airtable_educators(
        airtable_educators=airtable_educators,
        url_path_for=request.app.url_path_for)
