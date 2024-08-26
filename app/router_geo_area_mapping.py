import copy
import re
from typing import Union, Optional
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Request
import requests

from .airtable.client import AirtableClient
from .geocode.google_maps_client import GoogleMapsAPI
from .geocode import utils as geocode_utils
from .log import logger
from .models import auto_response_email_template
from .models import geo_areas as geo_area_models
from .models import geo_area_contacts as geo_area_contact_models
from .models import geo_area_target_communities as geo_area_target_community_models
from . import auth
from .utils.utils import get_airtable_client

from . import router_auto_response_email_templates

OPENAPI_TAG_METADATA = [
    {
        "name": geo_area_contact_models.MODEL_TYPE,
        "description": "Map RSEs to given cities/states/regions/countries/polygons",
    },
    {
        "name": geo_area_target_community_models.MODEL_TYPE,
        "description": "Map Target Communities to given cities/states/regions/countries/polygons",
    },
    {
        "name": geo_area_models.MODEL_TYPE,
        "description": "Map Geo Areas to given cities/states/regions/countries/polygons",
    },
]

router = APIRouter(
    prefix="/geo_mapping",
    tags=[],
    dependencies=[Depends(auth.JWTBearer(any_scope=["read:all", "read:educators"]))],
    responses={404: {"description": "Not found"}},
)

geo_area_router = APIRouter(
    prefix="/geographic_areas",
    tags=[geo_area_models.MODEL_TYPE],
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

geo_area_auto_response_email_template_router = APIRouter(
    prefix="/auto_response_email_templates",
    tags=[auto_response_email_template.MODEL_TYPE],
    dependencies=[Depends(auth.JWTBearer(any_scope=["read:all", "read:educators"]))],
    responses={404: {"description": "Not found"}},
)


def fetch_geo_area_wrapper(geo_area_id, airtable_client: AirtableClient):
    try:
        airtable_geo_area = airtable_client.get_geo_area_by_id(geo_area_id)
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Geographic Area not found")
        else:
            raise

    return airtable_geo_area


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


@geo_area_router.get("/", response_model=geo_area_models.ListAPIGeoAreaResponse, include_in_schema=False)
@geo_area_router.get("", response_model=geo_area_models.ListAPIGeoAreaResponse)
async def list_geo_areas(
    request: Request,
) -> geo_area_models.ListAPIGeoAreaResponse:
    airtable_client = get_airtable_client(request)
    airtable_geo_areas = airtable_client.list_geo_areas()

    data = geo_area_models.ListAPIGeoAreaData.from_airtable_geo_areas(
        airtable_geo_areas=airtable_geo_areas, url_path_for=request.app.url_path_for
    ).root

    return geo_area_models.ListAPIGeoAreaResponse(data=data, links={"self": request.app.url_path_for("list_geo_areas")})


@geo_area_router.get("/for_address", response_model=geo_area_models.APIGeoAreaResponse)
async def get_geo_area_given_address(request: Request, address: str):
    gmaps_client = GoogleMapsAPI()
    place = gmaps_client.geocode_address(address)

    if place is None:
        logger.warning(f"Unable to geocode address: {address}")

    geo_areas = await list_geo_areas(request)
    geo_area = geocode_utils.get_geo_area_nearest_to_place(place, geo_areas.data)

    return geo_area_models.APIGeoAreaResponse(
        data=geo_area,
        links={"self": f'{request.app.url_path_for("get_geo_area_given_address")}?{urlencode({"address": address})}'},
    )


@geo_area_router.get("/{geo_area_id}", response_model=geo_area_models.APIGeoAreaResponse)
async def get_geo_area(geo_area_id, request: Request):
    airtable_client = get_airtable_client(request)
    airtable_geo_area = fetch_geo_area_wrapper(geo_area_id, airtable_client)

    data = geo_area_models.APIGeoAreaData.from_airtable_geo_area(
        airtable_geo_area=airtable_geo_area, url_path_for=request.app.url_path_for
    )

    return geo_area_models.APIGeoAreaResponse(
        data=data,
        links={"self": request.app.url_path_for("get_geo_area", geo_area_id=geo_area_id)},
    )


@geo_area_target_community_router.get(
    "/", response_model=geo_area_contact_models.ListAPIGeoAreaContactResponse, include_in_schema=False
)
@geo_area_contacts_router.get("", response_model=geo_area_contact_models.ListAPIGeoAreaContactResponse)
async def list_geo_area_contacts(request: Request) -> geo_area_contact_models.ListAPIGeoAreaContactResponse:
    airtable_client = get_airtable_client(request)
    airtable_geo_area_contacts = airtable_client.list_geo_area_contacts()

    data = geo_area_contact_models.ListAPIGeoAreaContactData.from_airtable_geo_area_contacts(
        airtable_geo_area_contacts=airtable_geo_area_contacts, url_path_for=request.app.url_path_for
    ).root

    return geo_area_contact_models.ListAPIGeoAreaContactResponse(
        data=data, links={"self": request.app.url_path_for("list_geo_area_contacts")}
    )


@geo_area_contacts_router.get("/for_address", response_model=geo_area_contact_models.APIGeoAreaContactResponse)
async def get_geo_area_contact_given_address(request: Request, address: str, marketing_source: Union[str, None] = None):
    gmaps_client = GoogleMapsAPI()
    place = gmaps_client.geocode_address(address)

    if place is None:
        logger.warning(f"Unable to geocode address: {address}")

    geo_area_contacts = await list_geo_area_contacts(request)
    geo_area_contact = geocode_utils.get_geo_area_nearest_to_place(
        place=place, geo_areas=geo_area_contacts.data, marketing_source=marketing_source
    )

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
    ).root

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


@geo_area_auto_response_email_template_router.get(
    "/for_address", response_model=auto_response_email_template.APIAutoResponseEmailTemplateResponse
)
async def get_auto_response_email_templates_given_address(
    request: Request,
    address: str,
    contact_type: Union[str, None] = None,
    language: Union[str, None] = None,
    marketing_source: Union[str, None] = None,
):
    gmaps_client = GoogleMapsAPI()
    place = gmaps_client.geocode_address(address)

    def lower_and_remove_special_characters(string: Optional[str]) -> Optional[str]:
        if string is None:
            return None
        return re.sub(r"[\W_]", "", string).lower()

    if place is None:
        logger.warning(f"Unable to geocode address: {address}")

    auto_response_email_templates = await router_auto_response_email_templates.list_auto_response_email_templates(
        request
    )
    all_geo_areas = await list_geo_areas(request)

    def match_auto_response_email_templates(
        auto_responses: list[auto_response_email_template.APIAutoResponseEmailTemplateData],
        match_marketing_source: bool = True,
        match_language: bool = True,
        match_contact_type: bool = True,
    ):

        _contact_type = copy.copy(contact_type)
        _language = copy.copy(language)
        _marketing_source = copy.copy(marketing_source)

        if match_contact_type is False:
            _contact_type = None

        if match_language is False:
            _language = None

        if match_marketing_source is False:
            _marketing_source = None

        filtered_auto_response_email_templates = []
        for auto_response in auto_responses:
            if (
                (
                    (
                        _contact_type is not None
                        and lower_and_remove_special_characters(_contact_type)
                        == lower_and_remove_special_characters(auto_response.fields.contact_type)
                    )
                    or lower_and_remove_special_characters(auto_response.fields.contact_type) == "any"
                )
                and (
                    (
                        _language is not None
                        and lower_and_remove_special_characters(_language)
                        == lower_and_remove_special_characters(auto_response.fields.language)
                    )
                    or lower_and_remove_special_characters(auto_response.fields.language) in ["any", "english"]
                )
                and (
                    lower_and_remove_special_characters(_marketing_source)
                    == lower_and_remove_special_characters(auto_response.fields.marketing_source)
                )
            ):
                filtered_auto_response_email_templates.append(auto_response)

        filtered_geo_areas = []
        for geo_area in all_geo_areas.data:
            for auto_response in filtered_auto_response_email_templates:
                if geo_area.id in auto_response.fields.geographic_areas:
                    filtered_geo_areas.append(geo_area)

        auto_response_template = None
        if len(filtered_geo_areas) > 0:
            geo_area = geocode_utils.get_geo_area_nearest_to_place(place, filtered_geo_areas)

            if geo_area is not None:
                auto_response_template = list(
                    filter(lambda r: geo_area.id in r.fields.geographic_areas, filtered_auto_response_email_templates)
                )
                if len(auto_response_template) > 0:
                    auto_response_template = auto_response_template[0]
        return auto_response_template

    matched_template = match_auto_response_email_templates(
        auto_responses=auto_response_email_templates.data,
        match_marketing_source=True,
        match_language=True,
        match_contact_type=True,
    )

    if matched_template is None:
        matched_template = match_auto_response_email_templates(
            auto_responses=auto_response_email_templates.data,
            match_marketing_source=False,
            match_language=True,
            match_contact_type=True,
        )

    if matched_template is None:
        matched_template = match_auto_response_email_templates(
            auto_responses=auto_response_email_templates.data,
            match_marketing_source=False,
            match_language=False,
            match_contact_type=True,
        )

    if matched_template is None:
        matched_template = match_auto_response_email_templates(
            auto_responses=auto_response_email_templates.data,
            match_marketing_source=False,
            match_language=False,
            match_contact_type=False,
        )

    if matched_template is None:
        raise HTTPException(status_code=404, detail="No valid auto-response email template found for given address")

    return auto_response_email_template.APIAutoResponseEmailTemplateResponse(
        data=matched_template,
        links={"self": f'{request.app.url_path_for("get_geo_area_given_address")}?{urlencode({"address": address})}'},
    )


router.include_router(geo_area_router)
router.include_router(geo_area_contacts_router)
router.include_router(geo_area_target_community_router)
router.include_router(geo_area_auto_response_email_template_router)
