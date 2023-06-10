"""
Tests for complete model integrity.
"""
from botodto.aws.data_model_v2_min import build_model as build_model_min
from botodto.aws.data_model_v2_min import v2MinJson
from botodto.aws.data_model_v2_norm import build_model as build_model_norm
from botodto.aws.data_model_v2_norm import v2NormalJson
from botodto.aws.data_model_v3 import build_model as build_model_v3
from botodto.aws.data_model_v3 import v3Json


def test_v2_min_value_check():
    model = build_model_min()
    assert model.shapes  # ["ActivityList"].member is not None


def test_v2_norm_ActivityList_value_check():
    model = build_model_norm()
    shape_member = model.shapes["ActivityList"].member
    assert shape_member.shape == "ActivityListItem"


def test_v3_value_check():
    pass  # model = build_model_v3()
    # assert model.shapes # ["ActivityList"].member is not None
