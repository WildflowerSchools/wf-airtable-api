from typing import Dict, Optional
from pydantic import HttpUrl, RootModel

from app.airtable.base_model import BaseModel


class AirtableAttachmentThumbnailDetails(BaseModel):
    url: HttpUrl
    width: int
    height: int


class AirtableAttachmentThumbnails(RootModel):
    root: Dict[str, AirtableAttachmentThumbnailDetails]


class AirtableAttachment(BaseModel):
    id: str
    width: Optional[int] = None
    height: Optional[int] = None
    url: HttpUrl
    filename: str
    size: int
    type: str
    thumbnails: Optional[AirtableAttachmentThumbnails] = None
