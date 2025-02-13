from __future__ import annotations


from pydantic import BaseModel, root_validator

from ...api.schema_versioning import SchemaVersion
from ...api.service_name_mapping import MappedServiceName
from ...utils.json_utils import ingest_json
from ...utils.model_utils import listify_obj

__all__ = [
    "ShapeReference",
    "Shape",
    "HTTPInfo",
    "MemberInfo",
    "Output",
    "Operation",
    "Operations",
    "v2NormalJson",
    "read_source",
    "build_botocore",
]


class ShapeReference(BaseModel):
    shape: str
    # documentation: Optional[str]
    box: bool | None


class Shape(BaseModel):
    name: str
    type: str | None
    required: list[str] | None
    members: dict[str, ShapeReference] | None
    pattern: str | None
    member: ShapeReference | None
    box: bool | None
    sensitive: bool | None
    min: int | None
    max: int | None
    # documentation: Optional[str]
    enum: list[str] | None


class HTTPInfo(BaseModel):
    method: str
    requestUri: str


class MemberInfo(BaseModel):
    shape: str | None
    type: str | None


class Output(BaseModel):
    type: str


class Operation(BaseModel):
    name: str
    http: HTTPInfo
    input: ShapeReference
    output: ShapeReference
    errors: list[ShapeReference]
    # documentation: str
    idempotent: bool | None


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


def read_source(service_name: str | MappedServiceName) -> dict | list:
    service_name = MappedServiceName.ensure(service_name)
    return ingest_json(service_name=service_name, version=SchemaVersion.V2)


def build_botocore(service_name: str | MappedServiceName) -> v2NormalJson:
    j_norm = read_source(service_name)
    norm_model = v2NormalJson.parse_obj(j_norm)
    return norm_model
