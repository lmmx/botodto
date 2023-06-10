from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, root_validator

from ...utils.json_utils import ingest_json
from ...utils.model_utils import listify_obj


class ShapeReference(BaseModel):
    shape: str
    documentation: Optional[str]
    box: Optional[bool]


class Shape(BaseModel):
    name: str
    type: Optional[str]
    required: Optional[list[str]]
    members: Optional[dict[str, ShapeReference]]
    pattern: Optional[str]
    member: Optional[ShapeReference]
    box: Optional[bool]
    sensitive: Optional[bool]
    min: Optional[int]
    max: Optional[int]
    documentation: Optional[str]
    enum: Optional[list[str]]


class HTTPInfo(BaseModel):
    method: str
    requestUri: str


class MemberInfo(BaseModel):
    shape: Optional[str]
    type: Optional[str]


class Output(BaseModel):
    type: str


class Operation(BaseModel):
    name: str
    http: HTTPInfo
    input: ShapeReference
    output: ShapeReference
    errors: list[ShapeReference]
    documentation: str
    idempotent: Optional[bool]


class Operations(BaseModel):
    __root__: dict[str, Operation]


class v2NormalJson(BaseModel):
    version: float
    metadata: dict
    operations: Operations
    shapes: list[Shape]

    @root_validator(pre=True)
    def insert_shape_names(cls, values):
        return listify_obj(values=values, target_attr="shapes", key_alias="name")


def read_source():
    _norm_json = "v2-normal.json"
    j_norm = ingest_json(_norm_json)
    return j_norm


def build_model():
    j_norm = read_source()
    norm_model = v2NormalJson.parse_obj(j_norm)
    return norm_model
