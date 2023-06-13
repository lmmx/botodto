from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, root_validator

from ...utils.json_utils import ingest_json
from ...utils.model_utils import listify_obj


class ShapeType(Enum):
    BOOLEAN = "boolean"
    ENUM = "enum"
    FLOAT = "float"
    INTEGER = "integer"
    LIST = "list"
    LONG = "long"
    OPERATION = "operation"
    STRING = "string"
    STRUCTURE = "structure"
    TIMESTAMP = "timestamp"


class ShapeMember(BaseModel):
    type: Optional[ShapeType]
    member: Optional[ShapeMember]
    members: Optional[ShapeMember]


class NamedShapeMember(BaseModel):
    __root__: dict[str, Optional[ShapeMember]]


class Shape(BaseModel):
    name: str
    type: ShapeType
    required: Optional[list[str]]
    members: Optional[ShapeMember]
    pattern: Optional[str]
    # member: Optional[ShapeMember]
    box: Optional[bool]
    sensitive: Optional[bool]
    min: Optional[int]
    max: Optional[int]
    # documentation: Optional[str]
    enum: Optional[list[str]]


class Error(BaseModel):
    shape: str


class HTTPInfo(BaseModel):
    method: str
    requestUri: str


class MemberInfo(BaseModel):
    shape: Optional[str]
    type: Optional[str]


class Input(BaseModel):
    type: str
    required: Optional[list[str]]
    members: Optional[dict[str, Optional[MemberInfo]]]


class Output(BaseModel):
    type: str


class Operation(BaseModel):
    input: Optional[Input]
    output: Optional[Output]
    idempotent: Optional[bool]
    endpoint: Optional[dict[str, str]]


class Operations(BaseModel):
    __root__: dict[str, Operation]


class v2MinJson(BaseModel):
    version: float
    metadata: dict
    operations: Operations
    shapes: list[Shape]

    @root_validator(pre=True)
    def insert_shape_names(cls, values):
        return listify_obj(values=values, target_attr="shapes", key_alias="name")


def read_source():
    _min_json = "v2-min.json"
    j_min = ingest_json(_min_json)
    return j_min


def build_model():
    j_min = read_source()
    min_model = v2MinJson.parse_obj(j_min)
    return min_model
