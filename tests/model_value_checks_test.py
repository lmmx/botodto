"""
Tests for complete model integrity.
"""
from botodto.aws.models.v2_min import build_model as build_min
from botodto.aws.models.v2_min import v2MinJson
from botodto.aws.models.v2_norm import build_model as build_norm
from botodto.aws.models.v2_norm import v2NormalJson
from botodto.aws.models.v3 import build_model as build_v3
from botodto.aws.models.v3 import v3Json


def test_v2_min_value_check():
    model = build_min()
    assert isinstance(model, v2MinJson)
    assert model.shapes
    name = "Sd"
    al_shape = next((shape for shape in model.shapes if shape.name == name), None)
    assert al_shape is not None
    # It's not really covered but we don't care


def test_v2_norm_ActivityList_value_check():
    model = build_norm()
    assert isinstance(model, v2NormalJson)
    name = "ActivityList"
    al_shape = next(shape for shape in model.shapes if shape.name == name)
    shape_member = al_shape.member
    assert shape_member.shape == "ActivityListItem"


def test_v3_value_check():
    model = build_v3()
    assert isinstance(model, v3Json)
    first_shape = model.shapes[0]
    service_name = "com.amazonaws.sfn#AWSStepFunctions"
    service_shape = next(shape for shape in model.shapes if shape.name == service_name)
    assert first_shape is service_shape
    assert service_shape.type == "service"
    assert len(service_shape.operations) == 26
    assert service_shape.operations[0].target == "com.amazonaws.sfn#CreateActivity"
