import requests
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
async def list_educators(request: Request):
    airtable_client = request.state.airtable_client
    airtable_educators = airtable_client.list_educators()

    return educator_models.ListAPIEducatorResponse.from_airtable_educators(
        airtable_educators=airtable_educators,
        url_path_for=request.app.url_path_for)


@router.get("/{educator_id}", response_model=response_models.APIResponse)
async def get_educator(educator_id, request: Request):
    airtable_client = request.state.airtable_client
    airtable_educator = fetch_and_validate_educator(educator_id, airtable_client)

    return educator_models.APIEducatorResponse.from_airtable_educator(
        airtable_educator=airtable_educator,
        url_path_for=request.app.url_path_for)


@router.get("/{educator_id}/schools", response_model=response_models.ListAPIResponse)
async def get_educator_schools(educator_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_educator(educator_id, airtable_client)
    airtable_schools = airtable_client.get_schools_by_educator_id(educator_id)

    return school_models.ListAPISchoolResponse.from_airtable_schools(
        airtable_schools=airtable_schools,
        url_path_for=request.app.url_path_for)


@router.get("/{educator_id}/guides", response_model=response_models.ListAPIResponse)
async def get_educator_guides(educator_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_and_validate_educator(educator_id, airtable_client)
    airtable_partners = airtable_client.get_partners_by_educator_id(educator_id)

    return partner_models.ListAPIPartnerResponse.from_airtable_partners(
        airtable_partners=airtable_partners,
        url_path_for=request.app.url_path_for)


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
