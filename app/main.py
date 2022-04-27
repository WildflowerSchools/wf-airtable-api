import time
import logging
import random
import string

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from mangum import Mangum
import requests

from . import (
    auth,
    const,
    router_hubs,
    router_pods,
    router_schools,
    router_partners,
    router_educators,
    router_geo_area_mapping,
    router_ssj_typeforms,
    router_educators_schools,
)
from .airtable.client import AirtableClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stage = const.STAGE
root_path = f"/{stage}" if stage else ""
app = FastAPI(
    title="WF Airtable API",
    root_path=root_path,
    openapi_tags=[
        router_hubs.OPENAPI_TAG_METADATA,
        router_pods.OPENAPI_TAG_METADATA,
        router_schools.OPENAPI_TAG_METADATA,
        router_educators.OPENAPI_TAG_METADATA,
        router_partners.OPENAPI_TAG_METADATA,
        *router_geo_area_mapping.OPENAPI_TAG_METADATA,
        router_educators_schools.OPENAPI_TAG_METADATA,
    ],
)

token_auth_scheme = HTTPBearer()

origins = ["http://localhost", "http://localhost:3000", "http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


airtable_client = AirtableClient()


@app.middleware("http")
async def airtable_client_session_middleware(request: Request, call_next):
    request.state.airtable_client = airtable_client
    response = await call_next(request)
    return response


# DO NOT ATTEMPT TO CAPTURE REQUEST BODY HERE, IT WILL CAUSE THE APP TO FREEZE
@app.middleware("http")
async def log_request_timing(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    request.state.idem = idem

    logger.info(f"rid={idem} start request_path={request.url.path}")

    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(f"rid={idem} complete completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


async def log_request_details(request: Request):
    headers = "\r\n\t".join("{}: {}".format(k, v) for k, v in request.headers.items())
    body = await request.body()
    logger.info(
        """rid={rid} details
    {method} {url}

    HEADERS:
    {headers}

    BODY:
    {body}
    """.format(
            rid=request.state.idem, method=request.method, url=request.url, headers=headers, body=body.decode("utf-8")
        )
    )


def add_routers(routers):
    for r in routers:
        app.include_router(r, dependencies=[Depends(log_request_details)])


add_routers(
    [
        router_hubs.router,
        router_pods.router,
        router_schools.router,
        router_partners.router,
        router_educators.router,
        router_geo_area_mapping.router,
        router_ssj_typeforms.router,
        router_educators_schools.router,
    ]
)


@app.get("/")
async def hola_mundo():
    return JSONResponse(content={"message": "¡Hola, mundo!"})


@app.exception_handler(404)
async def resource_not_found(request, ex):
    return JSONResponse(status_code=404, content={"error": ex.detail if hasattr(ex, "detail") else "Not Found"})


@app.exception_handler(requests.exceptions.HTTPError)
async def airtable_resource_not_found(request, ex):
    if ex.response.status_code == 404:
        return JSONResponse(status_code=404, content={"error": "Airtable resource not found"})
    else:
        logger.exception(ex)
        return JSONResponse(status_code=ex.response.status_code, content=None)


@app.exception_handler(auth.AuthError)
async def handle_auth_error(request, ex):
    logger.exception(ex)
    return JSONResponse(status_code=ex.status_code, content=ex.error)


@app.exception_handler(Exception)
async def handle_general_exception(request, ex):
    logger.exception(ex)
    return JSONResponse(status_code=500, content="Unexpected server error")


handler = Mangum(app)
