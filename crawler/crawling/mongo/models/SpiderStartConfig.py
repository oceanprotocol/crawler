from typing import List
from pydantic import BaseModel, Field

from crawling.mongo.models.PyObjectId import PyObjectId


class FieldInfo(BaseModel):
    name: str = Field(...)
    no: int = Field(...)
    maxErrorsPermitted: int = Field(...)


class SpiderStartConfig(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    spiders: List[FieldInfo]
