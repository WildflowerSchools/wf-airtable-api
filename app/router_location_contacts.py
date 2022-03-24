import requests
from fastapi import APIRouter, Depends, HTTPException, Request

from .airtable.client import AirtableClient
from .models import response as response_models
from .models import location_contacts as location_contacts_models
from . import auth
from .utils.utils import get_airtable_client

OPENAPI_TAG_METADATA = {
    "name": location_contacts_models.MODEL_TYPE, "description": "First Contacts (RSEs and emails) for given cities/states/regions"
}

router = APIRouter(
    prefix="/location_contacts",
    tags=[location_contacts_models.MODEL_TYPE],
    dependencies=[Depends(auth.JWTBearer(any_scope=['read:all', 'read:educators']))],
    responses={404: {"description": "Not found"}}
)


def fetch_and_validate_location_contact(location_contact_id, airtable_client: AirtableClient):
    try:
        airtable_location_contact = airtable_client.get_location_contact_by_id(location_contact_id)
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Location Contact not found")
        else:
            raise

    return airtable_location_contact


# Dupe the root route to solve this issue: https://github.com/tiangolo/fastapi/issues/2060
@router.get("/", response_model=response_models.ListAPIResponse, include_in_schema=False)
@router.get("", response_model=response_models.ListAPIResponse)
async def list_location_contacts(request: Request):
    airtable_client = get_airtable_client(request)
    airtable_location_contacts = airtable_client.list_location_contacts()

    data = location_contacts_models.ListAPILocationContactData.from_airtable_location_contacts(
        airtable_location_contacts=airtable_location_contacts,
        url_path_for=request.app.url_path_for).__root__

    return response_models.ListAPIResponse(
        data=data,
        links={'self': request.app.url_path_for("list_location_contacts")}
    )


@router.get("/{location_contact_id}", response_model=response_models.APIResponse)
async def get_location_contact(location_contact_id, request: Request):
    airtable_client = get_airtable_client(request)
    airtable_location_contact = fetch_and_validate_location_contact(location_contact_id, airtable_client)

    data = location_contacts_models.APILocationContactData.from_airtable_location_contact(
        airtable_location_contact=airtable_location_contact,
        url_path_for=request.app.url_path_for)

    return response_models.APIResponse(
        data=data,
        links={'self': request.app.url_path_for("get_location_contact", location_contact_id=location_contact_id)}
    )
