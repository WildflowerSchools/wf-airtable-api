from urllib.parse import urlencode

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

OPENAPI_TAG_METADATA = {
    "name": school_models.MODEL_TYPE, "description": "Schools data"
}

router = APIRouter(
    prefix="/schools",
    tags=[school_models.MODEL_TYPE],
    dependencies=[Depends(auth.JWTBearer(any_scope=['read:all', 'read:schools']))],
    responses={404: {"description": "Not found"}}
)


def fetch_and_validate_school(school_id, airtable_client: AirtableClient):
    try:
        airtable_school = airtable_client.get_school_by_id(school_id)
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            raise HTTPException(status_code=404, detail="School not found")
        else:
            raise

    return airtable_school


# Dupe the root route to solve this issue: https://github.com/tiangolo/fastapi/issues/2060
@router.get("/", response_model=response_models.ListAPIResponse, include_in_schema=False)
@router.get("", response_model=response_models.ListAPIResponse)
async def list_schools(request: Request, page_size: str = 100, offset: str = ''):
    airtable_client = request.state.airtable_client
    airtable_schools, next_offset = airtable_client.list_schools(page_size=page_size, offset=offset)

    data = school_models.ListAPISchoolData.from_airtable_schools(
        airtable_schools=airtable_schools,
        url_path_for=request.app.url_path_for).__root__

    links = {
        'self': f'{request.app.url_path_for("list_schools")}?{urlencode({"page_size": page_size, "offset": offset})}'}
    if next_offset != '' and next_offset is not None:
        links['next'] = f'{request.app.url_path_for("list_schools")}?{urlencode({"page_size": page_size, "offset": next_offset})}'

    return response_models.ListAPIResponse(
        data=data,
        links=links,
        meta={"offset": next_offset})


@router.get("/{school_id}", response_model=response_models.APIResponse)
async def get_school(school_id, request: Request):
    airtable_client = request.state.airtable_client
    airtable_school = fetch_and_validate_school(school_id, airtable_client)

    if airtable_school is None:
        raise HTTPException(status_code=404, detail="School not found")

    data = school_models.APISchoolData.from_airtable_school(
        airtable_school=airtable_school,
        url_path_for=request.app.url_path_for)

    return response_models.APIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school", school_id=school_id)})


@router.get("/{school_id}/hub", response_model=response_models.APIResponse)
async def get_school_hub(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_hub = airtable_client.get_hub_by_school_id(school_id)

    if airtable_hub is None:
        raise HTTPException(status_code=404, detail="School Hub not found")

    data = hub_models.APIHubData.from_airtable_hub(
        airtable_hub=airtable_hub,
        url_path_for=request.app.url_path_for)

    return response_models.APIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_hub", school_id=school_id)})


@router.get("/{school_id}/pod", response_model=response_models.APIResponse)
async def get_school_pod(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_pod = airtable_client.get_pod_by_school_id(school_id)

    if airtable_pod is None:
        raise HTTPException(status_code=404, detail="School Pod not found")

    data = pod_models.APIPodData.from_airtable_pod(
        airtable_pod=airtable_pod,
        url_path_for=request.app.url_path_for)

    return response_models.APIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_pod", school_id=school_id)})


@router.get("/{school_id}/guides_and_entrepreneurs", response_model=response_models.ListAPIResponse)
async def get_school_guides_and_entrepreneurs(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_partners = airtable_client.get_guides_by_school_id(school_id)

    data = partner_models.ListAPIPartnerData.from_airtable_partners(
        airtable_partners=airtable_partners,
        url_path_for=request.app.url_path_for).__root__

    return response_models.ListAPIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_guides_and_entrepreneurs", school_id=school_id)})


@router.get("/{school_id}/primary_contacts", response_model=response_models.ListAPIResponse)
async def get_school_primary_contacts(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_educators = airtable_client.get_primary_contacts_by_school_id(school_id)

    data = educator_models.ListAPIEducatorData.from_airtable_educators(
        airtable_educators=airtable_educators,
        url_path_for=request.app.url_path_for).__root__

    return response_models.ListAPIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_primary_contacts", school_id=school_id)})


@router.get("/{school_id}/educators", response_model=response_models.ListAPIResponse)
async def get_school_educators(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_educators = airtable_client.get_all_educators_by_school_id(school_id)

    data = educator_models.ListAPIEducatorData.from_airtable_educators(
        airtable_educators=airtable_educators,
        url_path_for=request.app.url_path_for).__root__

    return response_models.ListAPIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_educators", school_id=school_id)})


@router.get("/{school_id}/current_educators", response_model=response_models.ListAPIResponse)
async def get_school_current_educators(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_educators = airtable_client.get_current_educators_by_school_id(school_id)

    data = educator_models.ListAPIEducatorData.from_airtable_educators(
        airtable_educators=airtable_educators,
        url_path_for=request.app.url_path_for).__root__

    return response_models.ListAPIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_current_educators", school_id=school_id)})


@router.get("/{school_id}/current_tls", response_model=response_models.ListAPIResponse)
async def get_school_current_tls(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_educators = airtable_client.get_current_tls_by_school_id(school_id)

    data = educator_models.ListAPIEducatorData.from_airtable_educators(
        airtable_educators=airtable_educators,
        url_path_for=request.app.url_path_for).__root__

    return response_models.ListAPIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_current_tls", school_id=school_id)})


@router.get("/{school_id}/founders", response_model=response_models.ListAPIResponse)
async def get_school_founders(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_educators = airtable_client.get_founders_by_school_id(school_id)

    data = educator_models.ListAPIEducatorData.from_airtable_educators(
        airtable_educators=airtable_educators,
        url_path_for=request.app.url_path_for).__root__

    return response_models.ListAPIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_founders", school_id=school_id)})
