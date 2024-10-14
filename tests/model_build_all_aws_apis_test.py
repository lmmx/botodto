"""
Tests for complete model integrity.
"""

from pytest import mark

from botodto.aws.models.v2_norm import build_model as build_norm
from botodto.aws.models.v2_norm import v2NormalJson
from botodto.utils.git.oa_repo import aws_oa_dir, clone_repository


@mark.skip(reason="Long running test, do not want to run it in normal suite")
def test_v2_norm_build():
    if not aws_oa_dir.exists():
        clone_repository()
    # TODO ingest the sources and check the model works for all services
    raise NotImplementedError
    model = build_norm()
    assert isinstance(model, v2NormalJson)
