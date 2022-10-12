from datetime import date
from typing import Dict, Optional
from pydantic import BaseModel, Field

from crawling.mongo.models.py_object_id import PyObjectId


class PaginationSettings(BaseModel):
    url: Optional[str] = Field(...)
    staticPagination: Optional[int] = Field(...)


class SourceSettings(BaseModel):
    paginationSettings: Optional[PaginationSettings]


class CrawlerConfig(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    baseURL: str = Field(...)
    createdDate: date = Field(...)
    updatedDate: date = Field(...)
    sourceSettings: Optional[SourceSettings]
    flowTimeouts: Optional[Dict[str, float]]
