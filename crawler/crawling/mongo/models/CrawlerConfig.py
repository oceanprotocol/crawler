from datetime import date
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from crawling.mongo.models.PyObjectId import PyObjectId


class PaginationType(str, Enum):
    havePageNumGetMaxItems = "havePageNumGetMaxItems"
    replaceInURL = "replaceInURL"


class FieldType(str, Enum):
    number = "number"
    string = "string"
    date = "date"


class Selectors(str, Enum):
    pagination = "pagination"
    maxItemsPagination = "maxItemsPagination"
    condoElementLink = "condoElementLink"
    condoList = "condoList"


class SelectorType(str, Enum):
    soup = "soup"
    jsSelector = "jsSelector"


class SelectorsValue(BaseModel):
    value: Optional[str]
    getFirstElement: bool = Field(...)
    classValue: Optional[str]
    titleValue: Optional[str]
    selectElement: Optional[str]
    type: SelectorType


class PaginationSettings(BaseModel):
    url: Optional[str] = Field(...)
    type: PaginationType
    staticPagination: Optional[int] = Field(...)


class FieldInfo(BaseModel):
    fieldName: str = Field(...)
    fieldType: FieldType
    fieldSelector: str = Field(...)


class SourceSettings(BaseModel):
    havePagination: bool = Field(...)
    haveInfiniteScroll: bool = Field(...)
    haveHTTP: bool = Field(...)
    flow: List[str]
    paginationSettings: Optional[PaginationSettings]
    selectors: Dict[Selectors, SelectorsValue]


class CrawlerConfig(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    sourceName: str = Field(...)
    sourceURL: str = Field(...)
    baseURL: str = Field(...)
    createdDate: date = Field(...)
    updatedDate: date = Field(...)
    fields: List[FieldInfo]
    sourceSettings: SourceSettings
    flowTimeouts: Optional[Dict[str, float]]
