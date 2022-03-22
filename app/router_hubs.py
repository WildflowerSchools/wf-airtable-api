import requests
from fastapi import APIRouter, Depends, Request, HTTPException

from .airtable.client import AirtableClient
from .models import response as response_models
from .models import hubs as hub_models
from .models import partners as partner_models
from .models import pods as pod_models
from .models import schools as school_models
from . import auth
from .utils.utils import get_airtable_client

router = APIRouter(
    prefix="/hubs",
    tags=[hub_models.MODEL_TYPE],
    dependencies=[Depends(auth.JWTBearer(any_scope=['read:all', 'read:educators', 'read:schools']))],
    responses={404: {"description": "Not found"}}
)


def fetch_and_validate_hub(hub_id, airtable_client: AirtableClient):
    try:
        airtable_hub = airtable_client.get_hub_by_id(hub_id)
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Hub not found")
        else:
            raise

    return airtable_hub


# Dupe the root route to solve this issue: https://github.com/tiangolo/fastapi/issues/2060
@router.get("/", response_model=response_models.ListAPIResponse, include_in_schema=False)
@router.get("", response_model=response_models.ListAPIResponse)
async def list_hubs(request: Request):
    airtable_client = get_airtable_client(request)
    airtable_hubs = airtable_client.list_hubs()

    data = hub_models.ListAPIHubData.from_airtable_hubs(
        airtable_hubs=airtable_hubs,
        url_path_for=request.app.url_path_for).__root__

    return response_models.ListAPIResponse(
        data=data,
        links={'self': request.app.url_path_for("list_hubs")}
    )


@router.get("/{hub_id}", response_model=response_models.APIResponse)
async def get_hub(hub_id, request: Request):
    airtable_client = get_airtable_client(request)
    airtable_hub = fetch_and_validate_hub(hub_id, airtable_client)

    data = hub_models.APIHubData.from_airtable_hub(
        airtable_hub=airtable_hub,
        url_path_for=request.app.url_path_for)

    return response_models.APIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_hub", hub_id=hub_id)}
    )


@router.get("/{hub_id}/regional_site_entrepreneurs", response_model=response_models.ListAPIResponse)
async def get_hub_site_entrepreneurs(hub_id, request: Request):
    airtable_client = get_airtable_client(request)
    fetch_and_validate_hub(hub_id, airtable_client)
    airtable_partners = airtable_client.get_partners_by_hub_id(hub_id)

    data = partner_models.ListAPIPartnerData.from_airtable_partners(
        airtable_partners=airtable_partners,
        url_path_for=request.app.url_path_for).__root__

    return response_models.ListAPIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_hub_site_entrepreneurs", hub_id=hub_id)}
    )


@router.get("/{hub_id}/pods", response_model=response_models.ListAPIResponse)
async def get_hub_pods(hub_id, request: Request):
    airtable_client = get_airtable_client(request)
    fetch_and_validate_hub(hub_id, airtable_client)
    airtable_pods = airtable_client.get_pods_by_hub_id(hub_id)

    data = pod_models.ListAPIPodData.from_airtable_pods(
        airtable_pods=airtable_pods,
        url_path_for=request.app.url_path_for).__root__

    return response_models.ListAPIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_hub_pods", hub_id=hub_id)}
    )


@router.get("/{hub_id}/schools", response_model=response_models.ListAPIResponse)
async def get_hub_schools(hub_id, request: Request):
    airtable_client = get_airtable_client(request)
    fetch_and_validate_hub(hub_id, airtable_client)
    airtable_schools = airtable_client.get_schools_by_hub_id(hub_id)

    data = school_models.ListAPISchoolData.from_airtable_schools(
        airtable_schools=airtable_schools,
        url_path_for=request.app.url_path_for).__root__

    return response_models.ListAPIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_hub_schools", hub_id=hub_id)}
    )
