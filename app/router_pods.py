import requests
from fastapi import APIRouter, Depends, Request, HTTPException

from .airtable.client import AirtableClient
from .models import response as response_models
from .models import hubs as hub_models
from .models import partners as partner_models
from .models import pods as pod_models
from .models import schools as school_models
from . import auth
from .utils.utils import get_airtable_client

OPENAPI_TAG_METADATA = {"name": pod_models.MODEL_TYPE, "description": "Pods data"}

router = APIRouter(
    prefix="/pods",
    tags=[pod_models.MODEL_TYPE],
    dependencies=[Depends(auth.JWTBearer(any_scope=["read:all", "read:educators", "read:schools"]))],
    responses={404: {"description": "Not found"}},
)


def fetch_pod_wrapper(pod_id, airtable_client: AirtableClient):
    try:
        airtable_pod = airtable_client.get_pod_by_id(pod_id)
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Pod not found")
        else:
            raise

    return airtable_pod


# Dupe the root route to solve this issue: https://github.com/tiangolo/fastapi/issues/2060
@router.get("/", response_model=pod_models.ListAPIPodResponse, include_in_schema=False)
@router.get("", response_model=pod_models.ListAPIPodResponse)
async def list_pods(request: Request):
    airtable_client = get_airtable_client(request)
    airtable_pods = airtable_client.list_pods()

    data = pod_models.ListAPIPodData.from_airtable_pods(
        airtable_pods=airtable_pods, url_path_for=request.app.url_path_for
    ).root

    return response_models.ListAPIResponse(data=data, links={"self": request.app.url_path_for("list_pods")})


@router.get("/{pod_id}", response_model=pod_models.APIPodResponse)
async def get_pod(pod_id, request: Request):
    airtable_client = get_airtable_client(request)
    airtable_pod = fetch_pod_wrapper(pod_id, airtable_client)

    data = pod_models.APIPodData.from_airtable_pod(airtable_pod=airtable_pod, url_path_for=request.app.url_path_for)

    return response_models.APIResponse(data=data, links={"self": request.app.url_path_for("get_pod", pod_id=pod_id)})


@router.get("/{pod_id}/hub", response_model=hub_models.APIHubResponse)
async def get_pod_hub(pod_id, request: Request):
    airtable_client = get_airtable_client(request)
    fetch_pod_wrapper(pod_id, airtable_client)
    airtable_hub = airtable_client.get_hub_by_pod_id(pod_id)

    if airtable_hub is None:
        raise HTTPException(status_code=404, detail="School Hub not found")

    data = hub_models.APIHubData.from_airtable_hub(airtable_hub=airtable_hub, url_path_for=request.app.url_path_for)

    return hub_models.APIHubResponse(data=data, links={"self": request.app.url_path_for("get_pod_hub", pod_id=pod_id)})


@router.get("/{pod_id}/contacts", response_model=partner_models.ListAPIPartnerResponse)
async def get_pod_contacts(pod_id, request: Request):
    airtable_client = get_airtable_client(request)
    fetch_pod_wrapper(pod_id, airtable_client)
    airtable_partners = airtable_client.get_partners_by_pod_id(pod_id)

    data = partner_models.ListAPIPartnerData.from_airtable_partners(
        airtable_partners=airtable_partners, url_path_for=request.app.url_path_for
    ).root

    return partner_models.ListAPIPartnerResponse(
        data=data, links={"self": request.app.url_path_for("get_pod_contacts", pod_id=pod_id)}
    )


@router.get("/{pod_id}/schools", response_model=school_models.ListAPISchoolResponse)
async def get_pod_schools(pod_id, request: Request):
    airtable_client = get_airtable_client(request)
    fetch_pod_wrapper(pod_id, airtable_client)
    airtable_schools = airtable_client.get_schools_by_pod_id(pod_id)

    data = school_models.ListAPISchoolData.from_airtable_schools(
        airtable_schools=airtable_schools, url_path_for=request.app.url_path_for
    ).root

    return school_models.ListAPISchoolResponse(
        data=data, links={"self": request.app.url_path_for("get_pod_schools", pod_id=pod_id)}
    )
