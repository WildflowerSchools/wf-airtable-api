from typing import Optional

import requests
from urllib.parse import urlencode, unquote

from fastapi import APIRouter, Depends, HTTPException, Request

from .airtable.client import AirtableClient
from .airtable.base_school_db import schools as airtable_school_models
from .models import educators as educator_models
from .models import hubs as hub_models
from .models import partners as partner_models
from .models import pods as pod_models
from .models import schools as school_models
from . import auth
from .utils.utils import get_airtable_client

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


def find_and_validate_schools(filters, airtable_client: AirtableClient):
    try:
        airtable_schools = airtable_client.find_schools(filters)
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Educator records not found")
        else:
            raise

    return airtable_schools


# Dupe the root route to solve this issue: https://github.com/tiangolo/fastapi/issues/2060
@router.get("/", response_model=school_models.ListAPISchoolResponse, include_in_schema=False)
@router.get("", response_model=school_models.ListAPISchoolResponse)
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

    return school_models.ListAPISchoolResponse(
        data=data,
        links=links,
        meta={"offset": next_offset})


@router.get("/find", response_model=school_models.ListAPISchoolResponse)
async def find_schools(request: Request,
                       organizational_unit: Optional[str] = None):
    airtable_client = get_airtable_client(request)

    filters = {}
    if organizational_unit:
        filters[airtable_school_models.AirtableSchoolFields.__fields__[
            'organizational_unit'].alias] = organizational_unit

    airtable_schools = find_and_validate_schools(filters, airtable_client)

    data = school_models.ListAPISchoolData.from_airtable_schools(
        airtable_schools=airtable_schools,
        url_path_for=request.app.url_path_for).__root__

    # Strip http://<<url>> from request.url, return just the <<path>>?<<query>>
    self_url = str(request.url)[(str(request.url).find(request.url.path)):]
    return school_models.ListAPISchoolResponse(
        data=data,
        links={'self': unquote(self_url)})


@router.get("/{school_id}", response_model=school_models.APISchoolResponse)
async def get_school(school_id, request: Request):
    airtable_client = request.state.airtable_client
    airtable_school = fetch_and_validate_school(school_id, airtable_client)

    if airtable_school is None:
        raise HTTPException(status_code=404, detail="School not found")

    data = school_models.APISchoolData.from_airtable_school(
        airtable_school=airtable_school,
        url_path_for=request.app.url_path_for)

    return school_models.APISchoolResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school", school_id=school_id)})


@router.get("/{school_id}/hub", response_model=hub_models.APIHubResponse)
async def get_school_hub(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_hub = airtable_client.get_hub_by_school_id(school_id)

    if airtable_hub is None:
        raise HTTPException(status_code=404, detail="School Hub not found")

    data = hub_models.APIHubData.from_airtable_hub(
        airtable_hub=airtable_hub,
        url_path_for=request.app.url_path_for)

    return hub_models.APIHubResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_hub", school_id=school_id)})


@router.get("/{school_id}/pod", response_model=pod_models.APIPodResponse)
async def get_school_pod(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_pod = airtable_client.get_pod_by_school_id(school_id)

    if airtable_pod is None:
        raise HTTPException(status_code=404, detail="School Pod not found")

    data = pod_models.APIPodData.from_airtable_pod(
        airtable_pod=airtable_pod,
        url_path_for=request.app.url_path_for)

    return pod_models.APIPodResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_pod", school_id=school_id)})


@router.get("/{school_id}/guides_and_entrepreneurs", response_model=partner_models.ListAPIPartnerResponse)
async def get_school_guides_and_entrepreneurs(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_partners = airtable_client.get_guides_by_school_id(school_id)

    data = partner_models.ListAPIPartnerData.from_airtable_partners(
        airtable_partners=airtable_partners,
        url_path_for=request.app.url_path_for).__root__

    return partner_models.ListAPIPartnerResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_guides_and_entrepreneurs", school_id=school_id)})


@router.get("/{school_id}/primary_contacts", response_model=educator_models.ListAPIEducatorResponse)
async def get_school_primary_contacts(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_educators = airtable_client.get_primary_contacts_by_school_id(school_id)

    data = educator_models.ListAPIEducatorData.from_airtable_educators(
        airtable_educators=airtable_educators,
        url_path_for=request.app.url_path_for).__root__

    return educator_models.ListAPIEducatorResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_primary_contacts", school_id=school_id)})


@router.get("/{school_id}/educators", response_model=educator_models.ListAPIEducatorResponse)
async def get_school_educators(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_educators = airtable_client.get_all_educators_by_school_id(school_id)

    data = educator_models.ListAPIEducatorData.from_airtable_educators(
        airtable_educators=airtable_educators,
        url_path_for=request.app.url_path_for).__root__

    return educator_models.ListAPIEducatorResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_educators", school_id=school_id)})


@router.get("/{school_id}/current_educators", response_model=educator_models.ListAPIEducatorResponse)
async def get_school_current_educators(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_educators = airtable_client.get_current_educators_by_school_id(school_id)

    data = educator_models.ListAPIEducatorData.from_airtable_educators(
        airtable_educators=airtable_educators,
        url_path_for=request.app.url_path_for).__root__

    return educator_models.ListAPIEducatorResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_current_educators", school_id=school_id)})


@router.get("/{school_id}/current_tls", response_model=educator_models.ListAPIEducatorResponse)
async def get_school_current_tls(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_educators = airtable_client.get_current_tls_by_school_id(school_id)

    data = educator_models.ListAPIEducatorData.from_airtable_educators(
        airtable_educators=airtable_educators,
        url_path_for=request.app.url_path_for).__root__

    return educator_models.ListAPIEducatorResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_current_tls", school_id=school_id)})


@router.get("/{school_id}/founders", response_model=educator_models.ListAPIEducatorResponse)
async def get_school_founders(school_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_school(school_id, airtable_client)
    airtable_educators = airtable_client.get_founders_by_school_id(school_id)

    data = educator_models.ListAPIEducatorData.from_airtable_educators(
        airtable_educators=airtable_educators,
        url_path_for=request.app.url_path_for).__root__

    return educator_models.ListAPIEducatorResponse(
        data=data,
        links={'self': request.app.url_path_for("get_school_founders", school_id=school_id)})
