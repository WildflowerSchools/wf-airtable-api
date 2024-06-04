from enum import Enum
from typing import Optional

from pydantic import Field

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse, ListAirtableResponse


class FieldCategoryType(str, Enum):
    race_ethnicity = "Race & Ethnicity"
    gender = "Gender"
    income_background = "Income Background As Child"
    household_income = "Household Income"
    educational_attainment = "Educational Attainment"
    pronouns = "Pronouns"
    languages = "Languages"
    montessori_certification_levels = "Montessori Certification Levels"
    montessori_certifiers = "Montessori Certifiers"
    montessori_certification_status = "Montessori Certification Status"
    lgbtqia = "LGBTQIA"
    classroom_levels = "Classroom Levels"


class AirtableFieldCategoriesFields(BaseModel):
    category: Optional[str] = Field(None, alias="Category ID")
    value: Optional[str] = Field(None, alias="Value")
    slug: Optional[str] = Field(None, alias="Slug")
    non_specific_category: Optional[bool] = Field(alias="Non-Specific Category", default=False)
    type: Optional[str] = Field(None, alias="Type")
    field_mappings: Optional[list[str]] = Field(None, alias="Field Mappings")


class AirtableFieldCategoriesResponse(AirtableResponse):
    fields: AirtableFieldCategoriesFields


class ListAirtableFieldCategoriesResponse(ListAirtableResponse):
    root: list[AirtableFieldCategoriesResponse]

    def get_records_for_field_category_ids(self, field_category_ids) -> "ListAirtableFieldCategoriesResponse":
        category_match = list(filter(lambda c: c.id in field_category_ids, self.root))
        return ListAirtableFieldCategoriesResponse(root=category_match)
