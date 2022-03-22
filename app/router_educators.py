import requests
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Request, HTTPException

from .airtable.client import AirtableClient
from .models import response as response_models
from .models import educators as educator_models
from .models import partners as partner_models
from .models import schools as school_models
from . import auth

router = APIRouter(
    prefix="/educators",
    tags=[educator_models.MODEL_TYPE],
    dependencies=[Depends(auth.JWTBearer(any_scope=['read:all', 'read:educators']))],
    responses={404: {"description": "Not found"}}
)


def fetch_and_validate_educator(educator_id, airtable_client: AirtableClient):
    try:
        airtable_educator = airtable_client.get_educator_by_id(educator_id)
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Educator not found")
        else:
            raise

    return airtable_educator


# Dupe the root route to solve this issue: https://github.com/tiangolo/fastapi/issues/2060
@router.get("/", response_model=response_models.ListAPIResponse, include_in_schema=False)
@router.get("", response_model=response_models.ListAPIResponse)
async def list_educators(request: Request, page_size: str = 100, offset: str = ''):
    airtable_client = request.state.airtable_client
    airtable_educators, next_offset = airtable_client.list_educators(page_size=page_size, offset=offset)

    data = educator_models.ListAPIEducatorData.from_airtable_educators(
        airtable_educators=airtable_educators,
        url_path_for=request.app.url_path_for).__root__

    links = {
        'self': f'{request.app.url_path_for("list_educators")}?{urlencode({"page_size": page_size, "offset": offset})}'}
    if next_offset != '' and next_offset is not None:
        links['next'] = f'{request.app.url_path_for("list_educators")}?{urlencode({"page_size": page_size, "offset": next_offset})}'

    return response_models.ListAPIResponse(
        data=data,
        links=links,
        meta={"offset": next_offset})


@router.get("/{educator_id}", response_model=response_models.APIResponse)
async def get_educator(educator_id, request: Request):
    airtable_client = request.state.airtable_client
    airtable_educator = fetch_and_validate_educator(educator_id, airtable_client)

    data = educator_models.APIEducatorData.from_airtable_educator(
        airtable_educator=airtable_educator,
        url_path_for=request.app.url_path_for)

    return response_models.APIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_educator", educator_id=educator_id)})


@router.get("/{educator_id}/schools", response_model=response_models.ListAPIResponse)
async def get_educator_schools(educator_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_educator(educator_id, airtable_client)
    airtable_schools = airtable_client.get_schools_by_educator_id(educator_id)

    data = school_models.ListAPISchoolData.from_airtable_schools(
        airtable_schools=airtable_schools,
        url_path_for=request.app.url_path_for).__root__

    return response_models.ListAPIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_educator_schools", educator_id=educator_id)})


@router.get("/{educator_id}/guides", response_model=response_models.ListAPIResponse)
async def get_educator_guides(educator_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_educator(educator_id, airtable_client)
    airtable_partners = airtable_client.get_partners_by_educator_id(educator_id)

    data = partner_models.ListAPIPartnerData.from_airtable_partners(
        airtable_partners=airtable_partners,
        url_path_for=request.app.url_path_for).__root__

    return response_models.ListAPIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_educator_guides", educator_id=educator_id)})


# @router.get("/{educator_id}/languages", response_model=response_models.APIResponse)
# async def get_educator_languages(educator_id, request: Request):
#     airtable_client = request.state.airtable_client
#     airtable_educator = airtable_client.get_educator_by_id(educator_id)
#
#     return educator_models.APIEducatorResponse.from_airtable_educator(
#         airtable_educator=airtable_educator,
#         url_path_for=request.app.url_path_for)
#
#
# @router.get("/{educator_id}/montessori_certifications", response_model=response_models.APIResponse)
# async def get_educator_montessori_certifications(educator_id, request: Request):
#     airtable_client = request.state.airtable_client
#     airtable_educator = airtable_client.get_educator_by_id(educator_id)
#
#     return educator_models.APIEducatorResponse.from_airtable_educator(
#         airtable_educator=airtable_educator,
#         url_path_for=request.app.url_path_for)
