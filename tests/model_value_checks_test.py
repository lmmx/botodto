"""
Tests for complete model integrity.
"""

from botodto.aws.models.v2_norm import build_model as build_v2
from botodto.aws.models.v2_norm import v2NormalJson
from botodto.aws.models.v3 import build_model as build_v3
from botodto.aws.models.v3 import v3Json


def test_v2_norm_ActivityList_value_check():
    model = build_v2("stepfunctions")
    assert isinstance(model, v2NormalJson)
    name = "ActivityList"
    al_shape = next(shape for shape in model.shapes if shape.name == name)
    shape_member = al_shape.member
    assert shape_member.shape == "ActivityListItem"


def test_v3_value_check():
    model = build_v3("stepfunctions")
    assert isinstance(model, v3Json)
    service_name = "AWSStepFunctions"
    domain_name = "com.amazonaws.sfn"
    source_name = f"{domain_name}#{service_name}"
    assert model.service.type == "service"
    assert model.service.name == service_name
    assert model.service.domain == domain_name
    assert model.service.source_name == source_name
    assert len(model.service.operations) == 26
    assert model.service.operations[0].target == "com.amazonaws.sfn#CreateActivity"
