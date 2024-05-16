from fastapi import APIRouter, Depends, Request

from . import auth
from .models import ssj_fillout_get_involved as ssj_fillout_get_involved_models
from .utils.utils import get_airtable_client

OPENAPI_TAG_METADATA = {
    "name": "SSJ Fillout",
    "description": "SSJ Fillout data in Airtable (mostly for storing responses)",
}

router = APIRouter(
    prefix="/ssj_fillout",
    tags=[ssj_fillout_get_involved_models.MODEL_TYPE],
    dependencies=[Depends(auth.JWTBearer(any_scope=["read:all", "read:educators", "read:schools"]))],
    responses={404: {"description": "Not found"}},
)


@router.post("/get_involved_response")
async def create_get_involved_response(
    payload: ssj_fillout_get_involved_models.CreateApiSSJFilloutGetInvolvedFields, request: Request
):
    airtable_client = get_airtable_client(request)

    airtable_payload = payload.to_airtable()
    airtable_response = airtable_client.create_fillout_get_involved_response(payload=airtable_payload)

    data = ssj_fillout_get_involved_models.ApiSSJFilloutGetInvolvedData.from_airtable(
        airtable_get_involved=airtable_response, url_path_for=request.app.url_path_for
    )

    return ssj_fillout_get_involved_models.ApiSSJFilloutGetInvolvedResponse(data=data, links=None)
