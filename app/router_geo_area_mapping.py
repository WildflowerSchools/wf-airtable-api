from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Request
import requests

from .airtable.client import AirtableClient
from .geocode.google_maps_client import GoogleMapsAPI
from .geocode import utils as geocode_utils
from .log import logger
from .models import geo_area_contacts as geo_area_contact_models
from .models import geo_area_target_communities as geo_area_target_community_models
from . import auth
from .utils.utils import get_airtable_client

OPENAPI_TAG_METADATA = [
    {
        "name": geo_area_contact_models.MODEL_TYPE,
        "description": "Map RSEs to given cities/states/regions/countries/polygons",
    },
    {
        "name": geo_area_target_community_models.MODEL_TYPE,
        "description": "Map Target Communities to given cities/states/regions/countries/polygons",
    },
]

router = APIRouter(
    prefix="/geo_mapping",
    tags=[],
    dependencies=[Depends(auth.JWTBearer(any_scope=["read:all", "read:educators"]))],
    responses={404: {"description": "Not found"}},
)

geo_area_contacts_router = APIRouter(
    prefix="/contacts",
    tags=[geo_area_contact_models.MODEL_TYPE],
    dependencies=[Depends(auth.JWTBearer(any_scope=["read:all", "read:educators"]))],
    responses={404: {"description": "Not found"}},
)

geo_area_target_community_router = APIRouter(
    prefix="/target_communities",
    tags=[geo_area_target_community_models.MODEL_TYPE],
    dependencies=[Depends(auth.JWTBearer(any_scope=["read:all", "read:educators"]))],
    responses={404: {"description": "Not found"}},
)


def fetch_geo_area_contact_wrapper(geo_area_contact_id, airtable_client: AirtableClient):
    try:
        airtable_geo_area_contact = airtable_client.get_geo_area_contact_by_id(geo_area_contact_id)
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Geographic Area Contact not found")
        else:
            raise

    return airtable_geo_area_contact


def fetch_geo_area_target_community_wrapper(geo_area_target_community_id, airtable_client: AirtableClient):
    try:
        airtable_geo_area_target_community = airtable_client.get_geo_area_target_community_by_id(
            geo_area_target_community_id
        )
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Geographic Area Target Community not found")
        else:
            raise

    return airtable_geo_area_target_community


@geo_area_target_community_router.get(
    "/", response_model=geo_area_contact_models.ListAPIGeoAreaContactResponse, include_in_schema=False
)
@geo_area_contacts_router.get("", response_model=geo_area_contact_models.ListAPIGeoAreaContactResponse)
async def list_geo_area_contacts(request: Request) -> geo_area_contact_models.ListAPIGeoAreaContactResponse:
    airtable_client = get_airtable_client(request)
    airtable_geo_area_contacts = airtable_client.list_geo_area_contacts()

    data = geo_area_contact_models.ListAPIGeoAreaContactData.from_airtable_geo_area_contacts(
        airtable_geo_area_contacts=airtable_geo_area_contacts, url_path_for=request.app.url_path_for
    ).__root__

    return geo_area_contact_models.ListAPIGeoAreaContactResponse(
        data=data, links={"self": request.app.url_path_for("list_geo_area_contacts")}
    )


@geo_area_contacts_router.get("/for_address", response_model=geo_area_contact_models.APIGeoAreaContactResponse)
async def get_geo_area_contact_given_address(request: Request, address: str):
    gmaps_client = GoogleMapsAPI()
    place = gmaps_client.geocode_address(address)

    if place is None:
        logger.warning(f"Unable to geocode address: {address}")

    geo_area_contacts = await list_geo_area_contacts(request)
    geo_area_contact = geocode_utils.get_geo_area_nearest_to_place(place, geo_area_contacts.data)

    return geo_area_contact_models.APIGeoAreaContactResponse(
        data=geo_area_contact,
        links={
            "self": f'{request.app.url_path_for("get_geo_area_contact_given_address")}?{urlencode({"address": address})}'
        },
    )


@geo_area_contacts_router.get(
    "/{geo_area_contact_id}", response_model=geo_area_contact_models.APIGeoAreaContactResponse
)
async def get_geo_area_contact(geo_area_contact_id, request: Request):
    airtable_client = get_airtable_client(request)
    airtable_geo_area_contact = fetch_geo_area_contact_wrapper(geo_area_contact_id, airtable_client)

    data = geo_area_contact_models.APIGeoAreaContactData.from_airtable_geo_area_contact(
        airtable_geo_area_contact=airtable_geo_area_contact, url_path_for=request.app.url_path_for
    )

    return geo_area_contact_models.APIGeoAreaContactResponse(
        data=data,
        links={"self": request.app.url_path_for("get_geo_area_contact", geo_area_contact_id=geo_area_contact_id)},
    )


@geo_area_target_community_router.get(
    "/", response_model=geo_area_target_community_models.ListAPIGeoAreaTargetCommunityResponse, include_in_schema=False
)
@geo_area_target_community_router.get(
    "", response_model=geo_area_target_community_models.ListAPIGeoAreaTargetCommunityResponse
)
async def list_geo_area_target_communities(
    request: Request,
) -> geo_area_target_community_models.ListAPIGeoAreaTargetCommunityResponse:
    airtable_client = get_airtable_client(request)
    airtable_geo_area_target_communities = airtable_client.list_geo_area_target_communities()

    data = geo_area_target_community_models.ListAPIGeoAreaTargetCommunityData.from_airtable_geo_area_target_communities(
        airtable_geo_area_target_communities=airtable_geo_area_target_communities, url_path_for=request.app.url_path_for
    ).__root__

    return geo_area_target_community_models.ListAPIGeoAreaTargetCommunityResponse(
        data=data, links={"self": request.app.url_path_for("list_geo_area_target_communities")}
    )


@geo_area_target_community_router.get(
    "/for_address", response_model=geo_area_target_community_models.APIGeoAreaTargetCommunityResponse
)
async def get_geo_area_target_community_given_address(request: Request, address: str):
    gmaps_client = GoogleMapsAPI()
    place = gmaps_client.geocode_address(address)

    if place is None:
        logger.warning(f"Unable to geocode address: {address}")

    geo_area_target_communities = await list_geo_area_target_communities(request)
    geo_area_target_community = geocode_utils.get_geo_area_nearest_to_place(place, geo_area_target_communities.data)

    return geo_area_target_community_models.APIGeoAreaTargetCommunityResponse(
        data=geo_area_target_community,
        links={
            "self": f'{request.app.url_path_for("get_geo_area_target_community_given_address")}?{urlencode({"address": address})}'
        },
    )


@geo_area_target_community_router.get(
    "/{geo_area_target_community_id}", response_model=geo_area_target_community_models.APIGeoAreaTargetCommunityResponse
)
async def get_geo_area_target_community(geo_area_target_community_id, request: Request):
    airtable_client = get_airtable_client(request)
    airtable_geo_area_target_community = fetch_geo_area_target_community_wrapper(
        geo_area_target_community_id, airtable_client
    )

    data = geo_area_target_community_models.APIGeoAreaTargetCommunityData.from_airtable_geo_area_target_community(
        airtable_geo_area_target_community=airtable_geo_area_target_community, url_path_for=request.app.url_path_for
    )

    return geo_area_target_community_models.APIGeoAreaTargetCommunityResponse(
        data=data,
        links={
            "self": request.app.url_path_for(
                "get_geo_area_target_community", geo_area_target_community_id=geo_area_target_community_id
            )
        },
    )


router.include_router(geo_area_contacts_router)
router.include_router(geo_area_target_community_router)
