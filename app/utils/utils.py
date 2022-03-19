from fastapi import Request

from ..airtable.client import AirtableClient


def get_airtable_client(request: Request) -> AirtableClient:
    return request.state.airtable_client
