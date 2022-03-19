from typing import Optional, Union

from pydantic import BaseModel


class APILinks(BaseModel):
    links: Optional[dict[str, Optional[str]]]


class APIData(BaseModel):
    id: str
    type: str
    meta: Optional[dict]


class APILinksAndData(APILinks):
    data: Optional[Union[str, APIData, list[Union[str, APIData]]]]


class APIRelationships(BaseModel):
    __root__: dict[str, Union[APILinksAndData, APILinks]]


class APIResponse(BaseModel):
    id: str
    type: str
    fields: dict
    relationships: APIRelationships
    links: dict[str, Optional[str]]


class ListAPIResponse(BaseModel):
    __root__: list[APIResponse]
