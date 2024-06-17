from typing import Optional

from pydantic import Field

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse, ListAirtableResponse


class AirtableAutoResponseEmailTemplate(BaseModel):
    geographic_areas: Optional[list[str]] = Field(None, alias="Geographic Areas")
    sendgrid_template_id: Optional[str] = Field(None, alias="Sendgrid Template ID")
    contact_type: Optional[str] = Field(None, alias="Contact Type")
    language: Optional[str] = Field(None, alias="Language")
    first_contact_email: Optional[str] = Field(None, alias="First Contact Email")
    marketing_source: Optional[str] = Field(None, alias="Marketing Source")


class AirtableAutoResponseEmailTemplateResponse(AirtableResponse):
    fields: AirtableAutoResponseEmailTemplate


class ListAirtableAutoResponseEmailTemplateResponse(ListAirtableResponse):
    root: list[AirtableAutoResponseEmailTemplateResponse]
