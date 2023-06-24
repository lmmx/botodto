from __future__ import annotations

from enum import Enum
from functools import partial
from pprint import pprint as _pprint
from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator

from ...api.schema_versioning import SchemaVersion
from ...api.service_name_mapping import MappedServiceName
from ...utils.json_utils import ingest_json
from ...utils.model_utils import listify_obj

__all__ = [
    "ShapeMember",
    "Pagination",
    "Range",
    "Endpoint",
    "AwsApiService",
    "SigV4",
    "XmlNamespace",
    "ServiceTrait",
    "Trait",
    "TargetTrait",
    "TraitWithNamedTarget",
    "SpecialShapeMember",
    "TargetReference",
    "SourcedName",
    "ServiceShape",
    "ShapeType",
    "StructShape",
    "GeneralShape",
    "HTTPInfo",
    "MemberInfo",
    "ShapeReference",
    "Output",
    "Operation",
    "Operations",
    "v3Json",
    "read_source",
    "check_rehydrate",
    "inspect_source",
    "view_shape_source",
    "view_shape_info",
    "build_model",
    "extract_shapes",
]

pprint = partial(_pprint, sort_dicts=False)


class ShapeMember(BaseModel):
    __root__: dict[str, Optional[str]]


class Pagination(BaseModel):
    inputToken: str
    outputToken: str
    items: str
    pageSize: str


class Range(BaseModel):
    min: Optional[int]
    max: Optional[int]


class Endpoint(BaseModel):
    hostPrefix: str


class AwsApiService(BaseModel):
    sdkId: str
    arnNamespace: str
    cloudFormationName: str
    cloudTrailEventSource: str
    endpointPrefix: str


class SigV4(BaseModel):
    name: str


class XmlNamespace(BaseModel):
    uri: str


class ServiceTrait(BaseModel):
    service: AwsApiService = Field(..., alias="aws.api#service")
    sigv4: SigV4 = Field(..., alias="aws.auth#sigv4")
    awsJson: dict = Field(..., alias="aws.protocols#awsJson1_0")
    # documentation: str = Field(..., alias="smithy.api#documentation")
    title: str = Field(..., alias="smithy.api#title")
    xmlNamespace: XmlNamespace = Field(..., alias="smithy.api#xmlNamespace")
    # endpointRuleSet: dict = Field(alias="smithy.rules#endpointRuleSet")


class Trait(BaseModel):
    pattern: Optional[str] = Field(alias="smithy.api#pattern")
    range: Optional[Range] = Field(alias="smithy.api#range")
    idempotent: Optional[dict] = Field(alias="smithy.api#idempotent")
    sensitive: Optional[dict] = Field(alias="smithy.api#sensitive")
    default: Optional[bool] = Field(alias="smithy.api#default")
    httpError: Optional[int] = Field(alias="smithy.api#httpError")
    length: Optional[Range] = Field(alias="smithy.api#length")
    paginated: Optional[Pagination] = Field(alias="smithy.api#paginated")
    error: Optional[Literal["client"]] = Field(alias="smithy.api#error")
    endpoint: Optional[Endpoint] = Field(alias="smithy.api#endpoint")


class TargetTrait(BaseModel):
    required: Optional[dict[str, str]] = Field(alias="smithy.api#required")
    enumValue: Optional[str] = Field(alias="smithy.api#enumValue")
    default: Optional[Any] = Field(alias="smithy.api#default")
    # documentation: str = Field(..., alias="smithy.api#documentation")


class TraitWithNamedTarget(BaseModel):
    target: str
    traits: Optional[TargetTrait]  # Optional[dict]  # Optional[dict[str, Trait]]


class SpecialShapeMember(BaseModel):
    __root__: dict[str, Optional[TraitWithNamedTarget]]


class TargetReference(BaseModel):
    target: str


class SourcedName(BaseModel):
    name: str
    domain: str
    source_name: str

    @root_validator(pre=True)
    def split_name(cls, values):
        if source_name := values.get("name"):
            values["source_name"] = source_name
            prefix, suffix = source_name.rsplit("#", 1)
            values["domain"] = prefix
            values["name"] = suffix
        return values


class ServiceShape(SourcedName):
    type: Literal["service"]
    version: str
    operations: list[TargetReference]
    traits: ServiceTrait


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


class StructShape(SourcedName):
    type: Literal["structure"]
    members: Optional[SpecialShapeMember]
    member: Optional[ShapeMember]
    errors: Optional[list[TargetReference]]
    input: Optional[TargetReference]
    output: Optional[TargetReference]
    traits: Optional[Trait]


class GeneralShape(SourcedName):
    type: ShapeType
    members: Optional[SpecialShapeMember]
    member: Optional[ShapeMember]
    errors: Optional[list[TargetReference]]
    input: Optional[TargetReference]
    output: Optional[TargetReference]
    traits: Optional[Trait]

    @validator("type")
    def evaluate_type(cls, v):
        return v.value


Shape = Union[StructShape, GeneralShape]

StructShape.update_forward_refs()


class HTTPInfo(BaseModel):
    method: str
    requestUri: str


class MemberInfo(BaseModel):
    shape: Optional[str]
    type: Optional[str]


class ShapeReference(BaseModel):
    shape: str


class Output(BaseModel):
    type: str


class Operation(BaseModel):
    name: str
    http: HTTPInfo
    input: ShapeReference
    output: ShapeReference
    errors: list[ShapeReference]
    # documentation: str
    idempotent: Optional[bool]


class Operations(BaseModel):
    __root__: dict[str, Operation]


class v3Json(BaseModel):
    smithy: float
    metadata: dict
    service: ServiceShape
    shapes: list[Shape]

    @root_validator(pre=True)
    def insert_shape_names(cls, values):
        values = listify_obj(values=values, target_attr="shapes", key_alias="name")
        # Assume the service will always be the 0'th in the list of shapes (and only!)
        values["service"] = values["shapes"].pop(0)
        return values


def read_source(service_name: str | MappedServiceName) -> dict | list:
    service_name = MappedServiceName.ensure(service_name)
    return ingest_json(service_name=service_name, version=SchemaVersion.JS_V3)


def check_rehydrate(model: BaseModel, source: dict) -> bool:
    rehydrated = model.dict(by_alias=True, exclude_unset=True)
    return rehydrated == source


def inspect_source():
    source = read_source()
    shape_it = iter(source["shapes"].items())
    next(shape_it)  # Discard service shape
    rest_of_shapes = [*shape_it]
    for s_name, s in rest_of_shapes:
        if "members" in s:
            members_info = s["members"]
            members_vals = list(members_info.values())
            members_vals_keys = [k for d in members_vals for k, v in d.items()]
            check = tuple([k in members_vals_keys for k in ["traits", "target"]])
            if check[0]:
                for subdict in members_vals:
                    if traits_dict := subdict.get("traits", {}):
                        traits_dict.pop("smithy.api#documentation", None)
                        if traits_dict:
                            try:
                                tt = TargetTrait.parse_obj(traits_dict)
                                rehydrate = check_rehydrate(tt, traits_dict)
                                if not rehydrate:
                                    print(f"Did not rehydrate {tt} into {traits_dict}")
                            except Exception as exc:
                                print(f"Raised {exc}")
                            pass
    return


def view_shape_source(shape_name="com.amazonaws.sfn#AWSStepFunctions"):
    j_smithy = read_source()
    return j_smithy["shapes"][shape_name]


def view_shape_info(shape_key: str = "operations", subkey: str | None = None):
    j_smithy = read_source()
    for v in [*j_smithy["shapes"].values()]:
        if v["type"] == "service" and shape_key in v:
            if subkey is None:
                print(v[shape_key])
            else:
                if subkey in v[shape_key]:
                    print(v[shape_key][subkey])


def build_model(service_name: MappedServiceName) -> v3Json:
    j_smithy = read_source(service_name)
    smithy_model = v3Json.parse_obj(j_smithy)
    return smithy_model


def extract_shapes():
    smithy_model = build_model()
    _shape_iterator = (v for v in smithy_model.shapes.values())
    service_shape = next(_shape_iterator)
    nonservice_shapes = [s for s in _shape_iterator]
    return service_shape, nonservice_shapes


# service_shape, nonservice_shapes = extract_shapes()
