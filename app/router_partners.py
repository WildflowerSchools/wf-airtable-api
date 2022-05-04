import requests
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Request

from .airtable.client import AirtableClient
from .models import response as response_models
from .models import educators as educator_models
from .models import hubs as hub_models
from .models import partners as partner_models
from .models import pods as pod_models
from .models import schools as school_models
from . import auth

OPENAPI_TAG_METADATA = {
    "name": partner_models.MODEL_TYPE,
    "description": "Partners data with role assignments, including RSEs, Guides, etc",
}

router = APIRouter(
    prefix="/partners",
    tags=[partner_models.MODEL_TYPE],
    dependencies=[Depends(auth.JWTBearer(any_scope=["read:all", "read:partners"]))],
    responses={404: {"description": "Not found"}},
)


def fetch_partner_wrapper(partner_id, airtable_client: AirtableClient):
    try:
        airtable_partner = airtable_client.get_partner_by_id(partner_id)
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Partner not found")
        else:
            raise

    return airtable_partner


# Dupe the root route to solve this issue: https://github.com/tiangolo/fastapi/issues/2060
@router.get("/", response_model=partner_models.ListAPIPartnerResponse, include_in_schema=False)
@router.get("", response_model=partner_models.ListAPIPartnerResponse)
async def list_partners(request: Request, page_size: str = 100, offset: str = ""):
    airtable_client = request.state.airtable_client
    airtable_partners, next_offset = airtable_client.list_partners(page_size=page_size, offset=offset)

    data = partner_models.ListAPIPartnerData.from_airtable_partners(
        airtable_partners=airtable_partners, url_path_for=request.app.url_path_for
    ).__root__

    links = {
        "self": f'{request.app.url_path_for("list_partners")}?{urlencode({"page_size": page_size, "offset": offset})}'
    }
    if next_offset != "" and next_offset is not None:
        links[
            "next"
        ] = f'{request.app.url_path_for("list_partners")}?{urlencode({"page_size": page_size, "offset": next_offset})}'

    return response_models.ListAPIResponse(data=data, links=links, meta={"offset": next_offset})


@router.get("/{partner_id}", response_model=partner_models.APIPartnerResponse)
async def get_partner(partner_id, request: Request):
    airtable_client = request.state.airtable_client
    airtable_partner = fetch_partner_wrapper(partner_id, airtable_client)

    data = partner_models.APIPartnerData.from_airtable_partner(
        airtable_partner=airtable_partner, url_path_for=request.app.url_path_for
    )

    return partner_models.APIPartnerResponse(
        data=data, links={"self": request.app.url_path_for("get_partner", partner_id=partner_id)}
    )


@router.get("/{partner_id}/hubs_as_entrepreneur", response_model=hub_models.ListAPIHubResponse)
async def get_partner_hubs_as_entrepreneur(partner_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_partner_wrapper(partner_id, airtable_client)
    airtable_hubs = airtable_client.get_hubs_by_entrepreneur_id(partner_id)

    data = hub_models.ListAPIHubData.from_airtable_hubs(
        airtable_hubs=airtable_hubs, url_path_for=request.app.url_path_for
    ).__root__

    return hub_models.ListAPIHubResponse(
        data=data, links={"self": request.app.url_path_for("get_partner_hubs_as_entrepreneur", partner_id=partner_id)}
    )


@router.get("/{partner_id}/pods_as_contact", response_model=pod_models.ListAPIPodResponse)
async def get_partner_pods_as_contact(partner_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_partner_wrapper(partner_id, airtable_client)
    airtable_pods = airtable_client.get_pods_by_contact_id(partner_id)

    data = pod_models.ListAPIPodData.from_airtable_pods(
        airtable_pods=airtable_pods, url_path_for=request.app.url_path_for
    ).__root__

    return pod_models.ListAPIPodResponse(
        data=data, links={"self": request.app.url_path_for("get_partner_pods_as_contact", partner_id=partner_id)}
    )


@router.get("/{partner_id}/schools_guiding", response_model=school_models.ListAPISchoolResponse)
async def get_guides_schools(partner_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_partner_wrapper(partner_id, airtable_client)
    airtable_schools = airtable_client.get_schools_by_guide_id(partner_id)

    data = school_models.ListAPISchoolData.from_airtable_schools(
        airtable_schools=airtable_schools, url_path_for=request.app.url_path_for
    ).__root__

    return school_models.ListAPISchoolResponse(
        data=data, links={"self": request.app.url_path_for("get_guides_schools", partner_id=partner_id)}
    )


@router.get("/{partner_id}/educators_guiding", response_model=educator_models.ListAPIEducatorResponse)
async def get_guides_educators(partner_id, request: Request):
    airtable_client = request.state.airtable_client
    fetch_partner_wrapper(partner_id, airtable_client)
    airtable_educators = airtable_client.get_educators_by_guide_id(partner_id)

    data = educator_models.ListAPIEducatorData.from_airtable_educators(
        airtable_educators=airtable_educators, url_path_for=request.app.url_path_for
    ).__root__

    return educator_models.ListAPIEducatorResponse(
        data=data, links={"self": request.app.url_path_for("get_guides_educators", partner_id=partner_id)}
    )
