import requests
from fastapi import APIRouter, Depends, HTTPException, Request

from .airtable.client import AirtableClient
from .airtable.base_start_school_first_contact.location_contacts import AirtableLocationLocationTypes
from .geocode.google_maps_client import GoogleMapsAPI
from .geocode import utils as geocode_utils
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
@router.get("/", response_model=location_contacts_models.ListAPILocationContactResponse, include_in_schema=False)
@router.get("", response_model=location_contacts_models.ListAPILocationContactResponse)
async def list_location_contacts(request: Request) -> response_models.ListAPIResponse:
    airtable_client = get_airtable_client(request)
    airtable_location_contacts = airtable_client.list_location_contacts()

    data = location_contacts_models.ListAPILocationContactData.from_airtable_location_contacts(
        airtable_location_contacts=airtable_location_contacts,
        url_path_for=request.app.url_path_for).__root__

    return location_contacts_models.ListAPILocationContactResponse(
        data=data,
        links={'self': request.app.url_path_for("list_location_contacts")}
    )


@router.get("/contact_for_address", response_model=location_contacts_models.APILocationContactResponse)
async def get_location_contact_given_address(request: Request, address: str):
    gmaps_client = GoogleMapsAPI()
    place = gmaps_client.geocode_address(address)

    if place is None:
        raise HTTPException(status_code=404, detail="Address not found")

    location_contacts = await list_location_contacts(request)

    default_location_contact = None
    default_international_location_contact = None
    city_location_contacts = []
    region_location_contacts = []
    state_location_contacts = []
    country_location_contacts = []
    for lc in location_contacts.data:
        if lc.fields.location_type == AirtableLocationLocationTypes.LOCATION_TYPE_DEFAULT_US:
            default_location_contact = lc

        elif lc.fields.location_type == AirtableLocationLocationTypes.LOCATION_TYPE_DEFAULT_INTERNATIONAL:
            default_international_location_contact = lc

        elif lc.fields.location_type == AirtableLocationLocationTypes.LOCATION_TYPE_CITY:
            city_location_contacts.append(lc)

        elif lc.fields.location_type == AirtableLocationLocationTypes.LOCATION_TYPE_REGION:
            region_location_contacts.append(lc)

        elif lc.fields.location_type == AirtableLocationLocationTypes.LOCATION_TYPE_STATE:
            state_location_contacts.append(lc)

        elif lc.fields.location_type == AirtableLocationLocationTypes.LOCATION_TYPE_COUNTRY:
            country_location_contacts.append(lc)

    location_contact = None
    for lc in city_location_contacts:
        if (geocode_utils.is_place_within_radius(place, lc.geocode(), lc.fields.city_radius)):
            location_contact = lc
            break

    if location_contact is None:
        for lc in region_location_contacts:
            if (geocode_utils.is_place_contained_within(place, lc.geocode())):
                location_contact = lc
                break

    if location_contact is None:
        for lc in state_location_contacts:
            if (geocode_utils.is_place_within_state(place, lc.geocode())):
                location_contact = lc
                break

    if location_contact is None:
        for lc in country_location_contacts:
            if (geocode_utils.is_place_within_country(place, lc.geocode())):
                location_contact = lc
                break

    if location_contact is None:
        if place.get_country_component().short_name == "US":
            location_contact = default_location_contact
        else:
            location_contact = default_international_location_contact

    return location_contacts_models.APILocationContactResponse(
        data=location_contact
    )


@router.get("/{location_contact_id}", response_model=location_contacts_models.APILocationContactResponse)
async def get_location_contact(location_contact_id, request: Request):
    airtable_client = get_airtable_client(request)
    airtable_location_contact = fetch_and_validate_location_contact(location_contact_id, airtable_client)

    data = location_contacts_models.APILocationContactData.from_airtable_location_contact(
        airtable_location_contact=airtable_location_contact,
        url_path_for=request.app.url_path_for)

    return location_contacts_models.APILocationContactResponse(
        data=data,
        links={'self': request.app.url_path_for("get_location_contact", location_contact_id=location_contact_id)}
    )
