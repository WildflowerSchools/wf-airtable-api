from typing import Optional, Union

from pydantic import Field, field_validator

from app.airtable.base_model import BaseModel
from app.airtable.base_school_db.field_categories import FieldCategoryType
from app.airtable.response import AirtableResponse, ListAirtableResponse
from app.airtable.validators import get_first_or_default_none


class AirtableFieldMappingFields(BaseModel):
    mapping: Optional[str] = Field(None, alias="Mapping ID")
    response: Optional[str] = Field(None, alias="Response")
    field_category_type: Optional[str] = Field(None, alias="Field Category Type")
    field_categories: Optional[list[str]] = Field(None, alias="Field Categories")

    @field_validator("field_category_type", mode="before")
    def _get_first_or_default_none(cls, v: Union[str, int, float]) -> Optional[Union[str, int, float]]:
        return get_first_or_default_none(v)

    # _get_first_or_default_none = validator("field_category_type", pre=True, allow_reuse=True)(get_first_or_default_none)


class AirtableFieldMappingResponse(AirtableResponse):
    fields: AirtableFieldMappingFields


class ListAirtableFieldMappingResponse(ListAirtableResponse):
    root: list[AirtableFieldMappingResponse]

    def map_response_value(
        self, field_category_type: FieldCategoryType, response_value
    ) -> Optional[AirtableFieldMappingResponse]:
        if response_value is None:
            return None

        def filter_mappings(mapping):
            return (
                mapping.fields.field_category_type.strip().lower() == field_category_type.strip().lower()
                and mapping.fields.response.strip().lower() == response_value.strip().lower()
            )

        mapping_match = list(filter(filter_mappings, self.root))
        if len(mapping_match) > 0:
            return mapping_match[0]

        return None
