from urllib.parse import unquote

import requests
from fastapi import APIRouter, Depends, HTTPException, Request, Query

from .airtable.client import AirtableClient
from .airtable.base_school_db.educators_schools import *
from .models import educators_schools as educator_school_models
from . import auth
from .utils.utils import get_airtable_client


OPENAPI_TAG_METADATA = {
    "name": educator_school_models.MODEL_TYPE, "description": "Educators_Schools many-to-many relationship data"
}


router = APIRouter(
    prefix="/educators_schools",
    tags=[educator_school_models.MODEL_TYPE],
    dependencies=[Depends(auth.JWTBearer(any_scope=['read:all', 'read:educators']))],
    responses={404: {"description": "Not found"}}
)


def fetch_and_validate_educator_school(educator_school_id, airtable_client: AirtableClient):
    try:
        airtable_educator_school = airtable_client.get_educator_school_by_id(educator_school_id)
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            raise HTTPException(status_code=404, detail="EducatorSchool not found")
        else:
            raise

    return airtable_educator_school


@router.get("/find", response_model=educator_school_models.ListAPIEducatorSchoolResponse)
async def find_educator_schools(request: Request,
                                educator_id: Optional[str] = Query(None),
                                school_id: Optional[str] = Query(None)):
    airtable_client = get_airtable_client(request)

    filters = {}
    if educator_id:
        filters[AirtableEducatorsSchoolsFields.__fields__['educator_id'].alias] = educator_id
    if school_id:
        filters[AirtableEducatorsSchoolsFields.__fields__['school_id'].alias] = school_id

    matches = airtable_client.find_educator_schools(filters=filters)

    data = educator_school_models.ListAPIEducatorSchoolData.from_airtable_educator_schools(
        airtable_educator_schools=matches,
        url_path_for=request.app.url_path_for).__root__

    # Strip http://<<url>> from request.url, return just the <<path>>?<<query>>
    self_url = str(request.url)[(str(request.url).find(request.url.path)):]
    return educator_school_models.ListAPIEducatorSchoolResponse(
        data=data,
        links={'self': unquote(self_url)})


@router.get("/{educator_school_id}", response_model=educator_school_models.APIEducatorSchoolResponse)
async def get_educator_school(educator_school_id, request: Request):
    airtable_client = get_airtable_client(request)
    airtable_educator_school = fetch_and_validate_educator_school(educator_school_id, airtable_client)

    data = educator_school_models.APIEducatorSchoolData.from_airtable_educator_school(
        airtable_educator_school=airtable_educator_school,
        url_path_for=request.app.url_path_for)

    return educator_school_models.APIEducatorSchoolResponse(
        data=data,
        links={'self': request.app.url_path_for("get_educator_school", educator_school_id=educator_school_id)})


@router.post("/", response_model=educator_school_models.APIEducatorSchoolResponse, include_in_schema=False)
@router.post("", response_model=educator_school_models.APIEducatorSchoolResponse)
async def create_educator_school(
        request: Request,
        payload: educator_school_models.CreateUpdateAPIEducatorSchoolFields):
    airtable_client = get_airtable_client(request)

    if payload.educator_id is None or payload.school_id is None:
        raise HTTPException(status_code=400, detail="Educator id and School id are both required")

    # Is educator_id + school_id pre-existing?
    filters = {
        AirtableEducatorsSchoolsFields.__fields__['educator_id'].alias: payload.educator_id,
        AirtableEducatorsSchoolsFields.__fields__['school_id'].alias: payload.school_id}
    existing = airtable_client.find_educator_schools(filters=filters).__root__
    if existing is not None and len(existing) > 0:
        raise HTTPException(status_code=409, detail="Educator and school are already linked")

    airtable_educator_schools_payload = payload.to_airtable_educator_schools()
    airtable_educator_schools_response = airtable_client.create_educator_schools(
        payload=airtable_educator_schools_payload)

    return airtable_educator_schools_response


@router.put("/{educator_school_id}", response_model=educator_school_models.APIEducatorSchoolResponse)
async def update_educator_school(
        educator_school_id,
        request: Request,
        payload: educator_school_models.CreateUpdateAPIEducatorSchoolFields):
    airtable_client = get_airtable_client(request)

    airtable_educator_schools_payload = payload.to_airtable_educator_schools()
    airtable_educator_schools_response = airtable_client.update_educator_schools(
        record_id=educator_school_id,
        payload=airtable_educator_schools_payload)
    return airtable_educator_schools_response
