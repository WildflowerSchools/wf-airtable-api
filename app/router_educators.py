import requests
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Request, HTTPException

from .airtable.client import AirtableClient
from .models import response as response_models
from .models import educators as educator_models
from .models import partners as partner_models
from .models import schools as school_models
from . import auth
from .utils.utils import get_airtable_client

OPENAPI_TAG_METADATA = {
    "name": educator_models.MODEL_TYPE, "description": "Educators data, including E/TLs and staff"
}

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
@router.get("/", response_model=educator_models.ListAPIEducatorResponse, include_in_schema=False)
@router.get("", response_model=educator_models.ListAPIEducatorResponse)
async def list_educators(request: Request, page_size: str = 100, offset: str = ''):
    airtable_client = get_airtable_client(request)
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


@router.post("/", response_model=educator_models.APIEducatorResponse, include_in_schema=False)
@router.post("", response_model=educator_models.APIEducatorResponse)
async def create_educator(
        payload: educator_models.CreateAPIEducatorFields,
        request: Request):
    airtable_client = get_airtable_client(request)

    if payload.email is None:
        raise HTTPException(status_code=400, detail="Educator email required")

    # Is educator pre-existing?
    pre_exists = len(airtable_client.get_educators_by_email(payload.email).__root__) > 0
    if pre_exists:
        if len(airtable_client.get_educators_by_email(payload.email).__root__) == 1:
            educator = airtable_client.get_educators_by_email(payload.email).__root__[0]
            airtable_client.add_typeform_start_a_school_response_to_educator(educator_id=educator.id,
                                                                             typeform_start_a_school_response_id=payload.start_a_school_response_id)
        raise HTTPException(status_code=409, detail="Educator already exists")

    # 1. Create the Educator
    airtable_educator_payload = payload.to_airtable_educator()
    airtable_educator_response = airtable_client.create_educator(payload=airtable_educator_payload)

    # 2. Create the Contact Info record (linked to educator)
    airtable_contact_info_payload = payload.to_airtable_contact_info(airtable_educator_response.id)
    airtable_client.create_contact_info(airtable_contact_info_payload)

    # 3. Create the Socio-economic record (linked to educator)
    airtable_socio_economic_payload = payload.to_airtable_socio_economic(airtable_educator_response.id)
    airtable_socio_economic_response = airtable_client.create_socio_economic(airtable_socio_economic_payload)

    # 4. Create the Language records (linked to socio-economic record)
    airtable_language_payloads = payload.to_airtable_languages(airtable_socio_economic_response.id)
    for l in airtable_language_payloads:
        airtable_client.create_language(l)

    # 5. Create the Montessori Certification records (linked to educator)
    airtable_montessori_certifications_payload = payload.to_airtable_montessori_certifications(
        airtable_educator_response.id)
    for m in airtable_montessori_certifications_payload:
        airtable_client.create_montessori_certification(m)

    return await get_educator(educator_id=airtable_educator_response.id, request=request)


@router.get("/{educator_id}", response_model=educator_models.APIEducatorResponse)
async def get_educator(educator_id, request: Request):
    airtable_client = get_airtable_client(request)
    airtable_educator = fetch_and_validate_educator(educator_id, airtable_client)

    data = educator_models.APIEducatorData.from_airtable_educator(
        airtable_educator=airtable_educator,
        url_path_for=request.app.url_path_for)

    return response_models.APIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_educator", educator_id=educator_id)})


@router.get("/{educator_id}/schools", response_model=school_models.ListAPISchoolResponse)
async def get_educator_schools(educator_id, request: Request):
    airtable_client = get_airtable_client(request)
    fetch_and_validate_educator(educator_id, airtable_client)
    airtable_schools = airtable_client.get_schools_by_educator_id(educator_id)

    data = school_models.ListAPISchoolData.from_airtable_schools(
        airtable_schools=airtable_schools,
        url_path_for=request.app.url_path_for).__root__

    return response_models.ListAPIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_educator_schools", educator_id=educator_id)})


@router.get("/{educator_id}/guides", response_model=partner_models.ListAPIPartnerResponse)
async def get_educator_guides(educator_id, request: Request):
    airtable_client = get_airtable_client(request)
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
