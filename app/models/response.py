from typing import Optional, Union

from pydantic import BaseModel


class APILinks(BaseModel):
    links: Optional[dict[str, Optional[str]]]


class APIDataBase(BaseModel):
    id: str
    type: str


class APIDataWithFields(BaseModel):
    id: str
    type: str
    fields: dict


class APILinksAndData(APILinks):
    data: Optional[Union[str, APIDataWithFields, APIDataBase, list[Union[str, APIDataWithFields, APIDataBase]]]]


class APIRelationships(BaseModel):
    __root__: dict[str, Union[APILinksAndData, APILinks]]


class APIData(APIDataWithFields):
    fields: dict
    relationships: APIRelationships
    links: dict[str, Optional[str]]


class APIResponse(APILinks):
    data: APIData
    meta: Optional[dict]


class ListAPIResponse(APIResponse):
    data: list[Union[APIData, dict]]
