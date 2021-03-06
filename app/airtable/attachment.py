from typing import Dict, Optional
from pydantic import HttpUrl

from app.airtable.base_model import BaseModel


class AirtableAttachmentThumbnailDetails(BaseModel):
    url: HttpUrl
    width: int
    height: int


class AirtableAttachmentThumbnails(BaseModel):
    __root__: Dict[str, AirtableAttachmentThumbnailDetails]


class AirtableAttachment(BaseModel):
    id: str
    width: Optional[int]
    height: Optional[int]
    url: HttpUrl
    filename: str
    size: int
    type: str
    thumbnails: Optional[AirtableAttachmentThumbnails]
