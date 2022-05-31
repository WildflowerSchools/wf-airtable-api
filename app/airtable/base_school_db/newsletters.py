from enum import Enum
from typing import Optional

from pydantic import Field

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse


class NewsletterSlugs(str, Enum):
    DISCOVERY_GROUP = "discovery_group"
    EMERGING_TEACHER_LEADER_GROUP = "etl_group"


class AirtableNewsletterFields(BaseModel):
    name: Optional[str] = Field(alias="Name")
    slug: Optional[str] = Field(alias="Slug")
    type: Optional[str] = Field(alias="Type")
    google_group_id: Optional[str] = Field(alias="Google Group ID")


class AirtableNewsletterResponse(AirtableResponse):
    fields: AirtableNewsletterFields


class ListAirtableNewsletterResponse(BaseModel):
    __root__: list[AirtableNewsletterResponse]
