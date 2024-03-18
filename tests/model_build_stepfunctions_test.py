"""
Tests for complete model integrity.
"""

from botodto.aws.models.v2_norm import build_model as build_norm
from botodto.aws.models.v2_norm import v2NormalJson
from botodto.aws.models.v3 import build_model as build_v3
from botodto.aws.models.v3 import v3Json


def test_v2_norm_build():
    model = build_norm(service_name="stepfunctions")
    assert isinstance(model, v2NormalJson)


def test_v3_build():
    model = build_v3(service_name="stepfunctions")
    assert isinstance(model, v3Json)
