from typing import Optional

from pydantic import BaseModel, Field, validator

from app.airtable.base_school_db.field_categories import FieldCategoryType
from app.airtable.response import AirtableResponse, ListAirtableResponse
from app.airtable.validators import get_first_or_default_none


class AirtableFieldMappingFields(BaseModel):
    mapping: Optional[str] = Field(alias="Mapping ID")
    response: Optional[str] = Field(alias="Response")
    field_category_type: Optional[str] = Field(alias="Field Category Type")
    field_categories: Optional[list[str]] = Field(alias="Field Categories")

    _get_first_or_default_none = validator(
        "field_category_type",
        pre=True,
        allow_reuse=True)(get_first_or_default_none)


class AirtableFieldMappingResponse(AirtableResponse):
    fields: AirtableFieldMappingFields


class ListAirtableFieldMappingResponse(ListAirtableResponse):
    __root__: list[AirtableFieldMappingResponse]

    def map_response_value(self, field_category_type: FieldCategoryType,
                           response_value) -> Optional[AirtableFieldMappingResponse]:
        def filter_mappings(mapping):
            return \
                mapping.fields.field_category_type.strip().lower() == field_category_type.strip().lower() and \
                mapping.fields.response.strip().lower() == response_value.strip().lower()

        mapping_match = list(filter(filter_mappings, self.__root__))
        if len(mapping_match) > 0:
            return mapping_match[0]

        return None
