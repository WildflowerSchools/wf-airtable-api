from typing import Optional

from pydantic import BaseModel, Field, root_validator

# class AirtableModel(BaseModel):
#     @root_validator(pre=True)
#     def extract_airtable(cls, values):
#         return {"id": values['id'], **values['fields']}


class School(BaseModel):
    id: str
    name: Optional[str] = Field(alias="Name")
    short_name: Optional[str] = Field(alias="Short Name")
    school_status: Optional[str] = Field(alias="School Status")
    school_startup_stage: Optional[str] = Field(alias="School Startup Stage")
    hubs: Optional['ListHub'] = Field(alias="Hub")
    pods: Optional['ListPod'] = Field(alias="Pod")


class ListSchool(BaseModel):
    __root__: list[School]


class Partner(BaseModel):
    id: str
    name: Optional[str] = Field(alias="Name")
    email: Optional[str] = Field(alias="Email")
    active: Optional[str] = Field(alias="Currently active")

    class Config:
        allow_population_by_field_name = True


class ListPartner(BaseModel):
    __root__: list[Partner]


class Pod(BaseModel):
    id: str
    name: Optional[str] = Field(alias="Name")
    pod_contacts: Optional[ListPartner] = Field(alias="Pod Contact")
    school_ids: Optional[list[str]] = Field(alias="School IDs")

    class Config:
        allow_population_by_field_name = True


class PodWithDependencies(Pod):
    schools: Optional[ListSchool] = Field(alias="Schools")


class ListPod(BaseModel):
    __root__: list[Pod]


class ListPodWithDependencies(BaseModel):
    __root__: list[PodWithDependencies]


class Hub(BaseModel):
    id: str
    name: Optional[str] = Field(alias="Name")
    regional_site_entrepreneurs: Optional[ListPartner] = Field(alias="Regional entrepreneur")
    pod_ids: Optional[list[str]] = Field(alias="Pod Assignment IDs")
    school_ids: Optional[list[str]] = Field(alias="School IDs")

    class Config:
        allow_population_by_field_name = True


class HubWithDependencies(Hub):
    pods: Optional[ListPod] = Field(alias="Pod Assignments")
    schools: Optional[ListSchool] = Field(alias="Schools")


class ListHub(BaseModel):
    __root__: list[Hub]


class ListHubWithDependencies(BaseModel):
    __root__: list[HubWithDependencies]


School.update_forward_refs()
