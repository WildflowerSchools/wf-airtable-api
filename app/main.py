import logging
import requests

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from mangum import Mangum

from . import auth, const, router_hubs, router_pods, router_schools, router_partners, router_educators, router_location_contacts, router_ssj_typeforms
from .airtable.client import AirtableClient

logger = logging.getLogger(__name__)

stage = const.STAGE
root_path = f"/{stage}" if stage else "/"
app = FastAPI(
    title="WF Airtable API",
    root_path=root_path,
    openapi_tags=[
        router_hubs.OPENAPI_TAG_METADATA,
        router_pods.OPENAPI_TAG_METADATA,
        router_schools.OPENAPI_TAG_METADATA,
        router_educators.OPENAPI_TAG_METADATA,
        router_partners.OPENAPI_TAG_METADATA,
        router_location_contacts.OPENAPI_TAG_METADATA
    ])

token_auth_scheme = HTTPBearer()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_hubs.router)
app.include_router(router_pods.router)
app.include_router(router_schools.router)
app.include_router(router_partners.router)
app.include_router(router_educators.router)
app.include_router(router_location_contacts.router)
app.include_router(router_ssj_typeforms.router)
airtable_client = AirtableClient()


@app.middleware("http")
async def airtable_client_session_middleware(request: Request, call_next):
    request.state.airtable_client = airtable_client
    response = await call_next(request)
    return response


@app.get("/")
async def hola_mundo():
    return JSONResponse(content={"message": '¡Hola, mundo!'})


@app.exception_handler(404)
async def resource_not_found(request, ex):
    return JSONResponse(status_code=404, content={"error": ex.detail if hasattr(ex, 'detail') else "Not Found"})


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
