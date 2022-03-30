from fastapi import APIRouter, Depends, Request

from . import auth
from .models import ssj_typeform_start_a_school as ssj_typeform_start_a_school_models
from .utils.utils import get_airtable_client

OPENAPI_TAG_METADATA = {
    "name": "SSJ Typeforms", "description": "SSJ Typeform data in Airtable (mostly for storing responses)"
}

router = APIRouter(
    prefix="/ssj_typeforms",
    tags=[ssj_typeform_start_a_school_models.MODEL_TYPE],
    dependencies=[Depends(auth.JWTBearer(any_scope=['read:all', 'read:educators', 'read:schools']))],
    responses={404: {"description": "Not found"}}
)


@router.post("/start_a_school_response")
async def create_start_a_school_response(
        payload: ssj_typeform_start_a_school_models.CreateApiSSJTypeformStartASchoolFields,
        request: Request):
    airtable_client = get_airtable_client(request)

    airtable_payload = payload.to_airtable()
    airtable_response = airtable_client.create_start_a_school_response(payload=airtable_payload)

    data = ssj_typeform_start_a_school_models.ApiSSJTypeformStartASchoolData.from_airtable(
        airtable_start_a_school=airtable_response,
        url_path_for=request.app.url_path_for)

    return ssj_typeform_start_a_school_models.ApiSSJTypeformStartASchoolResponse(
        data=data,
        links=None)
