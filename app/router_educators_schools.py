import requests
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from .airtable.client import AirtableClient
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
async def create_educator_school(request: Request):
    airtable_client = get_airtable_client(request)


@router.put("/{educator_school_id}", response_model=educator_school_models.APIEducatorSchoolResponse)
async def update_educator_school(educator_school_id, request: Request):
    airtable_client = get_airtable_client(request)
