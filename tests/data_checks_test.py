"""
Tests for basic model comparison of values.
"""
from botodto.aws import compare_sources


def test_stepfunction_key_comparison():
    norm_keys, min_keys, smithy_keys = compare_sources.run_comparison()
    assert min_keys == ["version", "metadata", "operations", "shapes"]
    assert [*min_keys, "documentation"] == norm_keys
    assert smithy_keys == ["smithy", "metadata", "shapes"]
